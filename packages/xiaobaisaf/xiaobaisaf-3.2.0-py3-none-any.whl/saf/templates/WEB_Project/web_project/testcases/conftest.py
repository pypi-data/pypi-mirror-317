#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/12/22 0:08
fileName    : conftest.py
'''
import base64
import pytest
import allure
from selenium import webdriver
from datetime import datetime
from ..config.bug_config import BUG_Config
from ..config.message_config import MSG_Config, FeiShu_Config, DingDing_Config
from ..common.BUG import ZenTaoService, JiraService
from ..common.Message import FeiShuService, DingDingService

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 提bug单、发送消息
            _CURRENT_TIME_ = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            _BUG_TITLE_ = f'{item.function.__name__}-{_CURRENT_TIME_}-测试失败'.replace('test_', '')
            _BUG_DOC_ = f'{item.function.__doc__}预期结果：passed<br>测试结果：{report.outcome}'.replace('\n', '<br>')
            try:
                _BUG_FIXER_ = list(
                    filter(lambda k_v: str(item.function.__name__)[5:] in k_v[1], BUG_Config.Bug_fix_table.items())
                )[0][0]
            except IndexError:
                _BUG_FIXER_ = ''
            if BUG_Config.Bug_Service_Name.lower() in ['zentao', '禅道']:
                if _BUG_FIXER_ == '':
                    _BUG_FIXER_ = ZenTaoService.account
                ZenTaoService().submit_bug(
                    title=_BUG_TITLE_,
                    steps=_BUG_DOC_,
                    assignedTo=ZenTaoService.assignedTo if ZenTaoService.assignedTo != '' else _BUG_FIXER_
                )
            elif BUG_Config.Bug_Service_Name.lower() in ['jira']:
                if _BUG_FIXER_ == '':
                    _BUG_FIXER_ = JiraService.username
                JiraService().submit_bug(
                    project_key='TEST',
                    summary=_BUG_TITLE_,
                    description=_BUG_DOC_,
                    project_id=10000,
                    assignee_name=JiraService.assignee if JiraService.assignee != '' else _BUG_FIXER_,
                )
            else:
                pass
            if FeiShu_Config._token_ != '':
                FeiShuService().sendRobot(f'{_BUG_TITLE_}\n\n{_BUG_DOC_}')
            if DingDing_Config._token_ != '':
                DingDingService().sendRobot(f'{_BUG_TITLE_}\n\n{_BUG_DOC_}')
            # 截图
            driver = item.funcargs.get('driver')
            if driver:
                image_base64 = driver.get_screenshot_as_base64()
                allure.attach(base64.b64decode(image_base64), name="截图", attachment_type=allure.attachment_type.PNG)
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % image_base64
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


@pytest.fixture(scope="session", autouse=True)
def driver():
    driver = webdriver.Chrome()
    yield driver
    if driver:
        driver.quit()