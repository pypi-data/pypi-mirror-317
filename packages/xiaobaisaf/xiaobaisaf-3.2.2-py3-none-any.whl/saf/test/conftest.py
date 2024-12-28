#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:23
@File  : conftest.py
'''
from saf.utils.BugUtils import addZenTaoBUG, addJiraBug
from saf.utils.SendMsgUtils import robotSendMessage
import pytest

TESTTYPE = 'feishu'

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
        if 'zentao' == TESTTYPE:
            doc = item.function.__doc__
            doc = str(doc).replace('\n', '<br>')
            addZenTaoBUG(title=item.function.__name__,
                          steps=f'{doc}预期结果：passed<br>测试结果：{report.outcome}')
        elif 'jira' == TESTTYPE:
            doc = item.function.__doc__
            addJiraBug(project_key='TEST', summary='xxx出现BUG', description=doc, project_id=10000, assignee_name='xiaobai')
        else:
            robotSendMessage(robot_name=TESTTYPE,
                             msg=f'测试脚本：{report.nodeid.split("::")[0]}\n测试用例：{report.nodeid.split("::")[1]}\n测试结果：{report.outcome}'
                             )