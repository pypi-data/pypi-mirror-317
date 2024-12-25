#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:23
@File  : conftest.py
'''
from saf import selenium_webdriver as webdriver
from saf.utils.BugUtils import addZenTaoBUG
from saf.utils.SendMsgUtils import robotSendMessage
import pytest
import allure
import base64

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
def _capture_screenshot():
    '''
    截图保存为base64，展示到html中
    :return:
    '''
    if driver:
        return driver.get_screenshot_as_base64()
    else:
        return '未截图'

@pytest.fixture(scope="session", autouse=True)
def browser():
    '''
        chrome的一些设置，有助测试，注释的部分自行选择
    '''
    Options = webdriver.ChromeOptions()
    Options.add_experimental_option('useAutomationExtension', False)      # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
    Options.add_experimental_option('excludeSwitches', ['--enable-automation'])  # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
    Options.add_experimental_option('detach', True)                       # 禁止自动关闭浏览器
    # Options.add_argument('--blink-settings=imagesEnabled=false')          # 隐藏图片
    # Options.add_argument('--no-sandbox')
    # Options.add_argument('--disable-dev-shm-usage')
    # Options.add_argument('--headless')                                    # 隐藏浏览器界面
    # Options.add_argument('--disable-gpu')
    Options.add_argument('--ignore-certificate-errors')
    Options.add_argument('--ignore-ssl-errors')
    # Options.add_argument('--disable-extensions')
    Options.add_argument('--disable-blink-features=AutomationControlled')   # 隐藏Webdriver特征
    driver = webdriver.Chrome(options=Options)
    driver.implicitly_wait(30)
    yield driver
    driver.quit()