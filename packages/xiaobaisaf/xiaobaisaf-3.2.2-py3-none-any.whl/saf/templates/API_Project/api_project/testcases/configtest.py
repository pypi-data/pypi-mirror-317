#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/12/3 18:28
fileName    : configtest.py
'''

import pytest
from datetime import datetime
from ..config.bug_config import BUG_Config
from ..config.message_config import MSG_Config, FeiShu_Config, DingDing_Config
from ..common.BUG import ZenTaoService, JiraService
from ..common.Message import FeiShuService, DingDingService

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    :param item     : 测试的单元对象
    :param call     : 测试的步骤：when（setup, call, teardown）三个步骤
    outcome         : 用例测试结果对象
    """
    outcome = yield
    report = outcome.get_result()
    if report.outcome == 'failed':
        _CURRENT_TIME_ =  datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
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