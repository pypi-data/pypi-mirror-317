#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/25 10:58
fileName    : IP.py
'''

import socket
from urllib.request import urlopen
from ..common.LOG import Logger

logger = Logger()

def get_local_ip():
    '''
    获取本机局域网IP
    :return: 局域网IP
    '''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        logger.info(f'获取本机局域网IP：{ip}')
        return ip
    except Exception as e:
        logger.error(f"获取局域网IP出错: {e}，默认返回：127.0.0.1")
        return '127.0.0.1'

def get_ip():
    '''
    获取本机公网IP
    :return: 公网IP
    '''
    try:
        ip = urlopen('https://ipinfo.io/ip').read().decode()
        logger.info(f'获取本机公网IP：{ip}')
        return ip
    except Exception as e:
        logger.error(f"获取本机公网IP出错: {e}，默认返回：0.0.0.0，建议使用局域网访问")
        return '0.0.0.0'

def check_port(port):
    '''
    检查端口是否被占用
    :param port: 端口号
    :return: True表示被占用，False表示未被占用
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((get_local_ip(), port))
            logger.info(f'端口{port}未使用')
            return False
        except socket.error:
            logger.info(f'端口{port}已被使用')
            return True
