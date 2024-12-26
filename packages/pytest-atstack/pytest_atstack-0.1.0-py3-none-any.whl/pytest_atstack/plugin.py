import os
import pytest


def pytest_addoption(parser):
    group = parser.getgroup("atstack")
    group.addoption(
        "--atstack",
        action="store_true",
        default=False,
        help="Enable special atstack behavior.",
    )


def get_markers(item: pytest.Item):
    markers = {}
    for mark in item.iter_markers():
        if mark.name == "allure_label":
            if mark.kwargs.get("label_type") == "owner":
                markers["owner"] = mark.args[0]
            elif mark.kwargs.get("label_type") == "severity":
                markers["severity"] = mark.args[0].value
    return markers


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    if item.config.getoption("--atstack"):
        report = outcome.get_result()
        error = str(report.longrepr) if report.outcome == "failed" else None
        result = {
            "status": report.outcome,
            "duration": report.duration,
            "error": error,
        }
        if not getattr(item, "atstack", None):
            title = getattr(getattr(item, "obj"), "__allure_display_name__")
            setattr(
                item,
                "atstack",
                {
                    "title": title,
                    "marks": get_markers(item),
                },
            )
        atstack = getattr(item, "atstack")
        atstack[report.when] = result


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item: pytest.Item, nextitem):
    _ = yield
    if item.config.getoption("--atstack"):
        stages = ["setup", "call", "teardown"]
        atstack = getattr(item, "atstack", {})
        # atstack["status"] = all(atstack[when].get("duration") for when in stages)
        atstack["duration"] = sum(atstack[when].get("duration") for when in stages)
        import json

        print(json.dumps(atstack, indent=2, ensure_ascii=False))
        print(os.environ.get("ATSTACK_TOKEN"))
