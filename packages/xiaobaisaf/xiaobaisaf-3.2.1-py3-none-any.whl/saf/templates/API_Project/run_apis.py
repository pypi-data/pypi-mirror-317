#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/18 23:28
fileName    : run_apis.py
'''
import pytest
import subprocess
from api_project import CASE_SCRIPT_DIR_PATH, DATA_DIR_PATH, REPORT_DIR_PATH
from api_project.common import init
from api_project.common.Network import check_port #, get_local_ip, get_ip
from api_project.common.Email import EmailService
from api_project.common.LOG import Logger
from api_project.config.allure_config import Allure

from threading import Thread

logger = Logger()

def allure_server():
    if not check_port(Allure.PORT):
        try:
            subprocess.Popen([Allure.PATH, 'serve', '-p', str(Allure.PORT), DATA_DIR_PATH],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)   # allure服务后台允许，允许局域网内访问
            logger.info(f"Allure服务正在监听：http://{Allure.IP}:{Allure.PORT}")
        except Exception as e:
            logger.error(f"Allure服务启动失败：{e}")


if __name__ == '__main__':
    init()    # 初始化数据，加载环境变量，例如：清空工作文件夹或文件，设置HOST地址

    # 执行用例
    pytest.main([
        CASE_SCRIPT_DIR_PATH,
        '-q',
        '-s',
        f'--alluredir={DATA_DIR_PATH}',
        '--clean-alluredir',
        f'--html={REPORT_DIR_PATH}/report.html',
        '--self-contained-html'
    ])

    t = Thread(target=allure_server)
    t.daemon = True
    t.start()

    # 发邮件，发送内容模板在email_config.py，可自行修改
    EmailService.send(
        # content=open(f'{REPORT_DIR_PATH}/report.html', 'r', encoding='utf-8').read(),
        # content_type='html',
        files=f'{REPORT_DIR_PATH}/report.html'
    )
