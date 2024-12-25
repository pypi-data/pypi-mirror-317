#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:23
@File  : conftest.py
'''
from saf import appium_webdriver as webdriver
from saf.utils.BugUtils import addZenTaoBUG
from saf.utils.SendMsgUtils import robotSendMessage
import pytest

TESTTYPE = ['sendMsg', 'submitBug'][0]

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    :param item     : 测试的单元对象
    :param call     : 测试的步骤：when（setup, call, teardown）三个步骤
    outcome         : 用例测试结果对象
    """
    outcome = yield                     # 获取每一条用例的执行结果
    report = outcome.get_result()
    if report.outcome == 'failed':
        if 'submitBug' == TESTTYPE:
            doc = item.function.__doc__
            doc = str(doc).replace('\n', '<br>')
            addZenTaoBUG(title=item.function.__name__,
                          steps=f'{doc}预期结果：passed<br>测试结果：{report.outcome}')
        elif 'endMsg' == TESTTYPE:
            robotSendMessage(robot_name='feishu',
                             msg=f'测试脚本：{report.nodeid.split("::")[0]}\n测试用例：{report.nodeid.split("::")[1]}\n测试结果：{report.outcome}'
                             )

@pytest.fixture(scope="session", autouse=True)
def mobile():
    global app
    if app is None:
        ANDROID_CAPS = {
            'automationName': 'uiautomator2',
            'platformName': 'Android',
            'platformVersion': '5.1',
            'deviceName': '设备名',
            'noReset': True,
            'allowClearUserData': 'true',
            'fullReset': "false",
            'exported': "true",
            'appPackage': '应用包名',
            'appActivity': '应用Activity名',
            'unicodeKeyboard': True,
            'resetKeyboard': True
        }

        IOS_CAPS = {
            'platformName': 'iOS',
            'platformVersion': '11.4',
            'deviceName': '设备名',
            'udid': '设备UDID',
            'bundleId': '应用包名',
            'noReset': True,
        }
        app = webdriver.Remote('http://127.0.0.1:4723/wd/hub', ANDROID_CAPS)
        yield app
        app.quit()