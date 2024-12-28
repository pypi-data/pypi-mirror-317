#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/21 11:11
fileName    : Email.py
'''
import smtplib
from typing import Union
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from ..config.email_config import EMail
from ..common.LOG import Logger

class EmailService(object):

    @classmethod
    def send(cls, content:str = EMail.Content_HTML, content_type: str = 'html', files : Union[str, list] = ''):
        logger = Logger()
        message = MIMEMultipart()
        message['From'] = EMail.SMTP_UserName
        message['To'] = ",".join(EMail.Receiver)
        message['Subject'] = Header(EMail.Subject_Title, 'utf-8')
        message.attach(MIMEText(content, content_type, 'utf-8'))

        attr_list = []
        if isinstance(files, str) and files != '' and ',' not in files:
            ''' 单个附件 '''
            attr_list.insert(0, files)
        elif isinstance(files, str) and ',' in files:
            ''' 多个附件 '''
            attr_list = files.split(',')
        elif isinstance(files, list):
            ''' 多个附件 '''
            attr_list = files
        if attr_list:
            for fpath in attr_list:
                _attr_ = MIMEText(open(fpath, 'rb').read(), 'base64', 'utf-8')  # 文件路径是这个代码附近的文件
                _attr_["Content-Type"] = 'application/octet-stream'
                _attr_["Content-Disposition"] = f'attachment; filename="{fpath}"'
                message.attach(_attr_)
                logger.info(f'已添加附件：{fpath}')
                del _attr_

        try:
            smtpObj = smtplib.SMTP_SSL(EMail.SMTP_HOST, EMail.SMTP_PORT)
            smtpObj.login(EMail.SMTP_UserName, EMail.SMTP_Passwd)
            smtpObj.sendmail(EMail.SMTP_UserName, EMail.Receiver, message.as_string())
            smtpObj.quit()
            logger.info("邮件已经发送成功")
        except Exception as e:
            logger.error(f'邮件发送失败！{e}')
