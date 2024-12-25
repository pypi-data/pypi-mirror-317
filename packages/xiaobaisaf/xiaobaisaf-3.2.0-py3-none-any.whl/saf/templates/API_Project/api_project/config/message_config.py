#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/12/2 14:30
fileName    : message_config.py
'''
from typing import Union, Any

class MSG_Config(object):
    app_name            : str = ''
    _token_             : str = ''
    webhook             : str = ''
    msg                 : str = ''
    msg_format          : dict = {}
    assert_jsonpath     : str = ''
    assert_value        : Union[Any] = None

class FeiShu_Config(MSG_Config):
    app_name :str = '飞书'
    _token_ : str = ''
    webhook_help_document = 'https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN'
    webhook : str = 'https://open.feishu.cn/open-apis/bot/v2/hook/' + _token_
    msg = 'Hello,FeiShu!'
    msg_format = {"msg_type": "text", "content": {"text": msg}}
    assert_jsonpath = "StatusCode"
    assert_value = 0

class DingDing_Config(MSG_Config):
    app_name  : str = '钉钉'
    _token_  : str = ''
    webhook_help_document = 'https://open.dingtalk.com/document/group/custom-robot-access'
    webhook  : str = 'https://oapi.dingtalk.com/robot/send?access_token=' + _token_
    msg = 'Hello,DingDing!'
    msg_format = {"msgtype": "text", "text": {"content": msg}}
    assert_jsonpath = 'errcode'
    assert_value = 0

