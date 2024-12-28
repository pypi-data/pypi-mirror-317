import random
import time

import allure
import pytest


@allure.parent_suite("Tests for web interface")
@allure.suite("Tests for essential features")
@allure.sub_suite("Tests for authentication")
@allure.epic("Web interface")
@allure.feature("Essential features")
@allure.story("Authentication")
@allure.title("Test Authentication")
@allure.description(
    "This test attempts to log into the website using a login and a password. Fails if any error happens.\n\nNote that this test does not test 2-Factor Authentication."
)
@allure.tag("NewUI", "Essentials", "Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
@allure.link("https://dev.example.com/", name="Website")
@allure.issue("AUTH-123")
@allure.testcase("TMS-456")
def test_allure_all_labels():
    value = random.randint(2, 4)
    time.sleep(value)
    assert 3 > value


@allure.title("测试标题1")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
def test_allure_labels():
    value = random.randint(2, 4)
    time.sleep(value)
    assert 3 > value


@pytest.mark.skip(reason="无条件跳过此测试")
@pytest.mark.owner("John Doe")
@pytest.mark.slow
def test_pytest_mark():
    value = random.randint(2, 4)
    time.sleep(value)
    assert 3 == value


def test_no_mark():
    value = random.randint(2, 4)
    time.sleep(value)
    assert 3 == value


def test_broken():
    value = random.randint(2, 4)
    time.sleep(value)
    raise Exception("出现了意外的错误")
