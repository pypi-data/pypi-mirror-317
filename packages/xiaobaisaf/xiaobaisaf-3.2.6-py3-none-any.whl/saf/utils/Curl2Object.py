#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/15 22:46
fileName    : Curl2Object.py
'''
import shlex
import os
from datetime import datetime
from re import match
from urllib.parse import urlparse

INDENT = 4
TAB_SPACE = INDENT * ' '
FEED = '\n' if os.name == 'nt' else '\r\n'

class Template(object):
    T1 = 'python_requests_pytest'
    T2 = 'python_requests_pytest_allure'

    INIT_HEADER_LIST = [
        '#! /usr/bin/env python',
        '# Description  ：本代码由周口小白职业培训学校自动化代码生成工具生成，请勿用于商业用途，如有问题请联系我们',
        '# Auther       : xiaobaiTser',
        '# Email        : 807447312@qq.com',
        f'# createTime  : {datetime.now().strftime("%Y/%m/%d %H:%M")}',
        ''
    ]

    T1_HEADER_LIST = INIT_HEADER_LIST + [
        'import requests',
        ''
    ]

    T2_HEADER_LIST = INIT_HEADER_LIST + [
        'import requests',
        'import pytest',
        'import allure',
        'from ..apis.Client import *',
        'from ..common.CSV import Reader',

    ]

    @classmethod
    def requests_template(cls, request: dict, add_import: bool = False) -> str:
        '''
        通过模板生成python_requests代码
        :param request: {'url': '', 'method': 'GET', 'headers': dict(), 'data': ''}
        :param add_import: False
        :return:
        import requests

        url = 'https://www.xiaobai.com/api/v1/login'
        headers = {'content-type':'application/json'}
        data = '{"username":"xiaobai", "password":"123456"}'
        response = requests.request(method='POST', url=url, headers=headers, data=data)

        assert 200 == response.json()['ErrorCode']
        ...
        '''

        code_line_list = [
            '',
            f"url = '{request.get('url')}'",
            f"headers = {request.get('headers')}",
            f"response = requests.request(method='{request.get('method')}', url=url, headers=headers, data=data, verify=False)",
            '',
            '# 断言',
            'assert 200 == response.status_code',
            ''
        ]
        if str(request.get('method')).upper() != 'GET':
            code_line_list.insert(3, f"data = '{request.get('data')}'")
        if add_import:
            code_line_list = cls.T1_HEADER_LIST + code_line_list
        return FEED.join(code_line_list)

    @classmethod
    def requests_pytest_allure_template(cls, api_name: str, request: dict, add_import: bool = True) -> str:
        '''
        通过模板生成python_requests_pytest代码
        :param api_name: ''
        :param request: {'url': '', 'method': 'GET', 'headers': dict(), 'data': ''}
        :param add_import: True
        :return:

        import os
        import pytest
        import allure
        from ..apis.Client import *
        from ..common.CSV import Reader
        from ..config.case_config import 接口名称_CASE_DATA_PATH

        # @allure.story('接口名称')
        @pytest.mark.parametrize(','.join(Reader(接口名称_CASE_DATA_PATH, False)[0]), Reader(接口名称_CASE_DATA_PATH, True))
        def test_接口名称(method, uri, headers, data):
            \'\'\'
                接口名称：
                接口域名：
                接口测试数据：
            \'\'\'
            allure.step('接口名称-请求')
            response = APIClient.session(method=method, url=os.environ.get('HOST') + uri, headers=headers, data=data)

            allure.step('接口名称-断言')
            json_assert(response, expression='code', value=0)

            # allure.step('接口名称-提取器')
            # json_extractor()
            ...
        '''
        API_NAME = api_name.upper()
        API_PARAMS_FOTMATER = ', '.join(request.keys())
        API_REQUEST_FORMATER = ', '.join(
            [f"{key}={key}" if key != 'headers' else "headers=eval(headers)" for key, value in request.items()])

        code_line_list = [
            f'from ..config.case_config import {API_NAME}_CASE_DATA_PATH',
            '',
            f'@allure.story("{API_NAME}")',
            f"@pytest.mark.parametrize('{API_PARAMS_FOTMATER}', Reader({API_NAME}_CASE_DATA_PATH, True))",
            f"def test_{API_NAME.lower()}({API_PARAMS_FOTMATER}):",
            f'{TAB_SPACE}"""',
            f"{TAB_SPACE}接口名称：{API_NAME}",
            f"{TAB_SPACE}接口域名：{os.environ.get('HOST')}",
            f"{TAB_SPACE}接口测试数据：{request}",
            f'{TAB_SPACE}"""',
            f"{TAB_SPACE}allure.step('{API_NAME}-请求')",
            f"{TAB_SPACE}response = APIClient.session({API_REQUEST_FORMATER})",
            f"{TAB_SPACE}",
            f"{TAB_SPACE}allure.step('{API_NAME}-断言')",
            f"{TAB_SPACE}assert response.status_code == 200"
            f"{TAB_SPACE}# json_assert(response, expression='jsonpath表达式', value=预期值)  # 依据接口文档修改",
            f"{TAB_SPACE}",
            f"{TAB_SPACE}# allure.step('{API_NAME}-提取器')",
            f"{TAB_SPACE}# json_extractor(response, env_name='变量名', expression='jsonpath表达式', index=0, default=默认值)",
            f"{TAB_SPACE}# 调用格式：os.environ.get('变量名')"
            ''
        ]
        if add_import:
            code_line_list = cls.T2_HEADER_LIST + code_line_list
        return FEED.join(code_line_list)

    @classmethod
    def requests_pytest_allure_template_at(cls, api_name: str, request: dict, add_import: bool = True) -> str:
        '''
        通过模板生成python_requests_pytest代码
        :param api_name: ''
        :param request: {'url': '', 'method': 'GET', 'headers': dict(), 'data': ''}
        :param add_import: True
        :return:

        import os
        import pytest
        import allure
        from ..apis.Client import *
        from ..common.CSV import Reader
        from ..config.case_config import 接口名称_CASE_DATA_PATH

        # @allure.story('接口名称')
        # @at_json_extractor(env_name='存储的变量名', expression='jsonpath表达式', index=0, default='缺省值')
        # @at_json_assert(expression='jsonpath表达式', index=0, value='预期值')
        @at_http_status_code_assert(code=200)
        @pytest.mark.parametrize(','.join(Reader(接口名称_CASE_DATA_PATH, False)[0]), Reader(接口名称_CASE_DATA_PATH, True))
        def test_接口名称(method, uri, headers, data):
            \'\'\'
                接口名称：
                接口域名：
                接口测试数据：
            \'\'\'
            allure.step('接口名称-请求')
            response = APIClient.session(method=method, url=os.environ.get('HOST') + uri, headers=eval(headers), data=data,
                                         auth_username='root', auth_password='r00t@xiaobaiaiservice')

            return response
            ...
        '''
        API_NAME = api_name.upper()
        API_PARAMS_FOTMATER = ', '.join(request.keys())
        API_REQUEST_FORMATER = ', '.join(
            [f"{key}={key}" if key != 'headers' else "headers=eval(headers)" for key, value in request.items()])

        code_line_list = [
            f'from ..config.case_config import {API_NAME}_CASE_DATA_PATH',
            '',
            f'@allure.story("{API_NAME}")',
            "# @at_json_extractor(env_name='存储的变量名', expression='jsonpath表达式', index=0, default='缺省值')",
            "# @at_json_assert(expression='jsonpath表达式', index=0, value='预期值')",
            '@at_http_status_code_assert(code=200)',
            f"@pytest.mark.parametrize('{API_PARAMS_FOTMATER}', Reader({API_NAME}_CASE_DATA_PATH, True))",
            f"def test_{API_NAME.lower()}({API_PARAMS_FOTMATER}):",
            f'{TAB_SPACE}"""',
            f"{TAB_SPACE}接口名称：{API_NAME}",
            f"{TAB_SPACE}接口域名：{os.environ.get('HOST')}",
            f"{TAB_SPACE}接口测试数据：{request}",
            f'{TAB_SPACE}"""',
            f"{TAB_SPACE}allure.step('{API_NAME}-请求')",
            f"{TAB_SPACE}response = APIClient.session({API_REQUEST_FORMATER})",
            f"{TAB_SPACE}",
            f"{TAB_SPACE}return response",
            '\n',
        ]
        if add_import:
            code_line_list = cls.T2_HEADER_LIST + code_line_list
        return FEED.join(code_line_list)

class Curl(object):
    def __init__(self):
        self.group        :list = []

    def str2obj(self, one_curl_str: str = ''):
        _request_: dict = {
            'api_name': '',
            'url': '',
            'method': 'GET',
            'headers': dict(),
        }
        one_curl_str = one_curl_str.strip().replace('^', '')
        try:
            args = shlex.split(one_curl_str)
            p_flag = False
            for index, arg in enumerate(args):
                arg = arg.replace('\n', '')
                if arg in ['-X', '--request']:
                    p_flag = True
                    _request_['method'] = args[index + 1]
                elif arg in ['-H', '--header'] and ':' in args[index + 1]:
                    p_flag = True
                    _request_['headers'][args[index + 1].split(':')[0]] = args[index + 1].split(':')[1].strip()
                elif arg in ['-d', '--data', '--data-ascii', '--data-raw', '--data-binary']:
                    p_flag = True
                    _request_['data'] = args[index + 1]
                    _request_['method'] = 'POST'
                else:
                    if not p_flag:
                        r = match(r'^[\^a-zA-Z]+?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f\^]))+$', arg)
                        if r:
                            # 分域名、路径、参数
                            _request_['url'] = urlparse(arg).path.replace(urlparse(os.environ['HOST']).path, '')
                            # 创建接口名称
                            _url_path_list_ = [p for p in urlparse(_request_['url']).path.split('/') if p]
                            if _url_path_list_:
                                if match('^[a-zA-Z]', _url_path_list_[-1]):
                                    _API_NAME_ = _url_path_list_[-1]
                                else:
                                    _API_NAME_ = '_' + _url_path_list_[-1]
                            else:
                                if 'INDEX_COUNT' not in os.environ.keys():
                                    os.environ['INDEX_COUNT'] = str(0)
                                else:
                                    os.environ['INDEX_COUNT'] = str(int(os.environ.get('INDEX_COUNT')) + 1)
                                _API_NAME_ = 'INDEX_' + os.environ.get('INDEX_COUNT')
                            _request_['api_name'] = _API_NAME_
                            if urlparse(arg).query:
                                _request_['params'] = urlparse(arg).query
                    p_flag = False
            self.group.append(_request_)
        except Exception as e:
            pass
        del _request_

    # @classmethod
    def load(self, curl_str: str = None, curl_file_path: str = None):
        '''
        加载curl字符串或者文件
        解析curl数据中的url、method、headers、cookies、data
        :param curl_str         :   CURL字符串
        :param curl_file_path   :   CURL文件(文本文件类型)
        :return:

        例如：
        Curl.load(curl_str="curl 'http://www.example.com/' -X 'GET'")
        Curl.load(curl_file_path="~/Desktop/curl_data.txt")
        '''
        if curl_str:
            if curl_str.count('curl ') == 1:
                curl_str = curl_str.replace('^', '')
                self.str2obj(curl_str[5:])
            elif curl_str.count('curl ') > 1:
                for curl in curl_str.split('curl ')[1:]:
                    self.str2obj(curl)
            else:
                pass
        elif curl_file_path and os.path.isfile(curl_file_path):
            with open(curl_file_path, 'r', encoding='utf-8') as f:
                curl_str = f.read()
                f.close()
            self.load(curl_str)
        else:
            pass
