#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/23 22:30
fileName    : LOG.py
'''
import os, sys
from datetime import datetime
from ..config.log_config import file_name
from .. import LOG_DIR_PATH

class Logger(object):
    def __init__(self):
        self.logfile = os.path.join(LOG_DIR_PATH, file_name)

    def logging(self, message, level, stream=sys.stdout, end='\n'):
        if level.lower() in ['debug', 'info', 'warning', 'error']:
            '''
            # ANSI 转义码
            ANSI_RESET = "\033[0m"
            ANSI_BOLD = "\033[1m"
            ANSI_UNDERLINE = "\033[4m"
            ANSI_BLACK = "\033[30m"
            ANSI_RED = "\033[31m"
            ANSI_GREEN = "\033[32m"
            ANSI_YELLOW = "\033[33m"
            ANSI_BLUE = "\033[34m"
            ANSI_MAGENTA = "\033[35m"
            ANSI_CYAN = "\033[36m"
            ANSI_WHITE = "\033[37m"
            使用： string = '{ANSI_RED}{text}{ANSI_RESET}'
            '''
            COLOR = {'debug': '\033[34m', 'info': '\033[37m', 'warning': '\033[33m', 'error': '\033[31m'}
            log = [
                COLOR[level.lower()],
                f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]',
                ' - ',
                f'[{level.upper()}]{(7-len(level)) * " "}',
                ' - ',
                f'{message}',
                end
            ]
            log_content =  ''.join(log)
            stream.write(log_content)
            if not os.path.exists(os.path.dirname(self.logfile)):
                os.makedirs(os.path.dirname(self.logfile))
            with open(self.logfile, 'a', encoding='utf-8') as f:
                f.write(log_content[5:])
                f.close()
        else:
            raise ValueError(f"无效的日志level: {level}, 有效level范围是：'debug', 'info', 'warning', 'error'")

    def info(self, message: str = ''):
        self.logging(message, level='INFO')

    def INFO(self, message: str = ''):
        self.logging(message, level='INFO')

    def error(self, message: str = ''):
        self.logging(message, level='ERROR', stream=sys.stderr)

    def ERROR(self, message: str = ''):
        self.logging(message, level='ERROR', stream=sys.stderr)

    def warning(self, message: str = ''):
        self.logging(message, level='WARNING')

    def WARNING(self, message: str = ''):
        self.logging(message, level='WARNING')

    def debug(self, message: str = ''):
        self.logging(message, level='DEBUG')

    def DEBUG(self, message: str = ''):
        self.logging(message, level='DEBUG')
