#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/20 22:22
@File  : __init__.py
'''
from typing import Union
import datetime

# 将pip更新源设置为：https://pypi.tuna.tsinghua.edu.cn/simple
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

from selenium import webdriver as selenium_webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # 键盘事件
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标事件
from loguru import logger
# 运行日志
# logger.add(sink='auto_info_{time}.log', rotation='1 day')

from requests import request, Session
from appium import webdriver as appium_webdriver
from jmespath import search
from yaml import full_load

# 当前版本的httpx，只有在异步请求时才略优于requests，此处可使用到发送消息使用
# from httpx import request