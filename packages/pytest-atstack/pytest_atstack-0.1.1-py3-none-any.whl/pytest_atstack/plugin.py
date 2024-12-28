import json
import logging
import os
from typing import List, Literal, TypeAlias

import pytest

Status: TypeAlias = Literal["passed", "failed", "skipped", "broken", "unkown"]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def pytest_addoption(parser):
    group = parser.getgroup("atstack")
    group.addoption(
        "--atstack",
        action="store_true",
        default=False,
        help="Enable special atstack behavior.",
    )


def get_allure_markers(markers: dict, mark: pytest.Mark) -> dict:
    label_type = mark.kwargs.get("label_type")
    match label_type:
        case "owner":
            markers.setdefault("owner", mark.args[0])
        case "severity":
            severity = getattr(mark.args[0], "value", None)
            markers.setdefault("severity", severity)
        case "tag":
            markers.setdefault("tag", list(mark.args))
    return markers


def get_markers(item: pytest.Item) -> dict:
    markers = {}
    for mark in item.iter_markers():
        try:
            match mark.name:
                case "allure_label":
                    get_allure_markers(markers, mark)
                case "owner":
                    markers.setdefault("owner", mark.args[0])
        except (IndexError, KeyError, AttributeError):
            logging.warning(f"can not found test label for {item.name}")
            continue
    return markers


def is_atstack(item: pytest.Item) -> bool | tuple[str, str]:
    atstack = item.config.getoption("--atstack")
    token = os.environ.get("ATSTACK_PROJECT_TOKEN", None)
    id = os.environ.get("ATSTACK_REPORT_ID", None)
    return token, id if all([atstack, token, id]) else False


def get_status(status: List[str]) -> Status:
    for state in status:
        if state != "passed":
            return state
    return "passed"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    if not is_atstack(item):
        return
    report = outcome.get_result()
    error = str(report.longrepr) if report.outcome == "failed" else None
    result = {
        "status": report.outcome,
        "duration": report.duration,
        "error": error,
    }
    if not getattr(item, "atstack", None):
        title_name = "__allure_display_name__"
        title = item.name
        try:
            title = getattr(getattr(item, "obj"), title_name)
        except AttributeError:
            logging.warning("can not found allure title for test %s" % item.name)
        content = {"title": title, "marks": get_markers(item)}
        setattr(item, "atstack", content)
    atstack = getattr(item, "atstack")
    atstack[report.when] = result


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item: pytest.Item, nextitem):
    _ = yield
    if not is_atstack(item):
        return
    stages = ["setup", "call", "teardown"]
    atstack = getattr(item, "atstack", {})
    status = [atstack[when].get("status") for when in stages if when in atstack]
    atstack["status"] = get_status(status)
    duration = sum(atstack.get(when, {}).get("duration", 0) for when in stages)
    atstack["duration"] = "{:.2f}".format(duration)
    print(json.dumps(atstack, indent=2, ensure_ascii=False))
    token, id = is_atstack(item)
