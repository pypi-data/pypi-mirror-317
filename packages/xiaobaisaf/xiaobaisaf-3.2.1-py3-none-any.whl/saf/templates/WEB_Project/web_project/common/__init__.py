#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/18 23:27
fileName    : __init__.py.py
'''

import os
import shutil
from .. import (
    DATA_DIR_PATH,
    REPORT_DIR_PATH,
    ALLURE_REPORT_DIR_PATH,
    LOG_DIR_PATH,
    PROJECT_CLEAN
)
from .ENV import ENV
from ..config.host_config import HOST
from .LOG import Logger

logger = Logger()

def _clean(path:str = None):
    '''
    清空文件及或者删除指定的文件
    :param path: 文件夹或者文件
    :return:
    '''
    path = os.path.abspath(path)
    if os.path.isdir(path):
        try:
            shutil.rmtree(path)
            logger.info(f'[{path}]\t文件夹已经清空完毕~')
        except Exception as e:
            logger.error(str(e))
        if not os.path.exists(path):
            os.mkdir(path)
            logger.info(f'[{path}]\t文件夹已经创建完毕~')
    elif os.path.isfile(path):
        try:
            os.remove(path)
            logger.info(f'[{path}]\t文件已经删除完毕~')
        except Exception as e:
            logger.error(str(e))

def clean():
    ''' 清除上次执行的数据 '''

    if PROJECT_CLEAN.data_status:
        _clean(DATA_DIR_PATH)
    if PROJECT_CLEAN.report_status:
        _clean(REPORT_DIR_PATH)
    if PROJECT_CLEAN.allure_report_status:
        _clean(ALLURE_REPORT_DIR_PATH)

def init():
    ''' 初始化 '''
    clean()
    ENV.load()
    ENV.set_env('HOST', HOST.CURRENT_HOST)
    logger.info('初始化完毕~')