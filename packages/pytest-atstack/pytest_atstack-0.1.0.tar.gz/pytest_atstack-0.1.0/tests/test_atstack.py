import allure
import time
import random


@allure.title("测试标题1")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
def test_1():
    value = random.randint(1, 5)
    time.sleep(value)
    assert 3 > value


@allure.title("测试标题2")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
def test_2():
    value = random.randint(1, 5)
    time.sleep(value)
    assert 3 < value


@allure.title("测试标题3")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "John Doe")
def test_3():
    value = random.randint(1, 5)
    time.sleep(value)
    assert 3 == value
