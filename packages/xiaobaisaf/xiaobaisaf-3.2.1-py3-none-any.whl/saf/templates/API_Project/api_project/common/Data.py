#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/26 7:58
fileName    : Data.py
'''

import glob
import os
import json
from jsonpath import jsonpath
from .. import DATA_DIR_PATH
from ..common.Network import get_ip, get_local_ip
from ..config.allure_config import Allure

def get_all_case_result():
    '''
    获取所有api运行结果:
    名称、时间、状态
    {'用例名称': {'time': 时间, 'status': 状态}}
    '''
    all_result = {}
    all_result_files = glob.iglob(os.path.join(DATA_DIR_PATH, '*-result.json'), recursive=True)
    for file_path in all_result_files:
        content = json.load(open(file_path, 'r', encoding='utf-8'))
        case_name = jsonpath(content, '$..fullName')[0].split('#')[0]
        case_time = float((int(jsonpath(content, '$..stop')[0]) - int(jsonpath(content, '$..start')[0])) / 1000)
        case_status = jsonpath(content, '$..status')[0]
        if case_name not in all_result.keys():
            all_result[case_name] = {'time': case_time, 'status': case_status}
    return all_result

def get_case_result_html():
    '''
    将所有接口结果写入HTML代码，用于邮件发送
    :return:
    '''
    all_case_result_str = ''
    for k, v in get_all_case_result().items():
        if v['status'] == 'passed':
            all_case_result_str += f'<tr><td class="case_name">{k}</td><td class="case_time">{v["time"]}</td><td class="case_result green_text">通过</td></tr>'
        elif v['status'] == 'failed':
            all_case_result_str += f'<tr><td class="case_name">{k}</td><td class="case_time">{v["time"]}</td><td class="case_result red_text">失败</td></tr>'
    return f'''
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>\
.center{{margin:auto;width:60%;padding:10px;text-align:center;border:3px solid green}}\
.case_name{{color:#696969}}.case_time{{color:#808080}}.red_text{{color:red}}.green_text{{color:green}}\
</style></head><body class="center"><h2>👇测试结果👇</h2><br>\
<table class="center" style="width:100%"><thead><tr><th class="case_name_title" style="width:60%">\
<b>执行接口名称</b></th><th class="case_time_title" style="width:20%"><b>时间</b></th>\
<th class="case_result_title" style="width:100%"><b>结果</b></th></tr></thead>\
<tbody>{all_case_result_str}</tbody></table><br>\
<div id="report"><span id="1"><a href="http://{get_local_ip()}:{Allure.PORT}"style="text-decoration: none;">\
点击查看局域网Allure报告(<span class="red_text">若服务在公网服务器，此处无效</span>)</a><br>\
<a href="http://{get_ip()}:{Allure.PORT}"style="text-decoration: none;">点击查看公网Allure报告(<span class="red_text">\
若服务在内网服务器，此处无效</span>)</a><br></span><br><span>附件🏷为pytest的html报告</span></div><body></html>
'''