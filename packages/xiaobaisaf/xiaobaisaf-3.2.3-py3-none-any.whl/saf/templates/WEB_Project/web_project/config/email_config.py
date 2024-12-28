#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/21 14:48
fileName    : email_config.py
'''

from ..common.Data import get_case_result_html

class EMail(object):
    # QQ的SMTP服务域名
    _QQ_SMTP_HOST_      : str = 'smtp.qq.com'
    _163_SMTP_HOST_     : str = 'smtp.163.com'
    # SMTP服务域名或者IP
    SMTP_HOST           : str = _QQ_SMTP_HOST_
    # SMTP端口号
    SMTP_PORT           : int = 465
    # 邮箱登录用户名
    SMTP_UserName       : str = '807447312@qq.com'
    # 邮箱密码或者授权码
    SMTP_Passwd         : str = '授权码或者密码'
    # 邮件标题
    Subject_Title       : str = '自动化测试'
    # 收件人
    Receiver            : list = ['807447312@qq.com']
    # 邮件内容
    Content_HTML        : str = get_case_result_html()

