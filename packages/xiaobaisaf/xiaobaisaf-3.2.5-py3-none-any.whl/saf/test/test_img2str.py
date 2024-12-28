#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/28 23:40
@File  : test_element.py
'''
from selenium import webdriver as selenium_webdriver
from saf.utils.ElementUtils import find_element
from saf.utils.CaptchaUtils import image2str

c = selenium_webdriver.Chrome()
c.get('http://mail.xiaobai.com:8080/Center/Index/login')
find_element(driver=c, value='//*[@name="captcha"]').send_keys(image2str(driver=c, value='//*[@id="captcha"]'))