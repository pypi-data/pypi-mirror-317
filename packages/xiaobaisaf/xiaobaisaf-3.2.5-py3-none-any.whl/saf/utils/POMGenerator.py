#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import ssl
from argparse import ArgumentParser
from time import sleep
from os import path, remove
from bs4 import BeautifulSoup
from lxml import etree
from pypinyin import lazy_pinyin
# 判断selenium版本不能低于4
from selenium import __version__
from sympy.utilities.misc import func_name

if __version__ < "4":
    os.system("pip install selenium -U")
    exit(0)
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ssl._create_default_https_context = ssl._create_unverified_context

class PageListener(object):
    def __init__(
        self,
        start_url: str = "",
        dirname: str = "",
        rewrite: bool = True,
        elements: str = "",
        exclude_elements: str = "",
    ):
        """
        基于Selenium基础操作过程中将每页内容转为POM
        :param start_url            : 首页URL地址
        :param dirname              : 代码输出目录
        :param rewrite              : 是否覆盖旧文件
        :param elements             : 自定义元素
        :param exclude_elements     : 自定义排除元素
        :return
        """
        self.PY_FILE_NAME_LIST = []
        self.PROJECT_PATH = dirname
        if rewrite and path.exists(self.PROJECT_PATH):
            try:
                remove(self.PROJECT_PATH)
            except PermissionError as e:
                pass
        if not path.exists(self.PROJECT_PATH):
            os.makedirs(self.PROJECT_PATH)
        Options = webdriver.ChromeOptions()
        Options.add_experimental_option("useAutomationExtension", False)
        Options.add_experimental_option("excludeSwitches", ["--enable-automation"])
        Options.add_argument("--disable-blink-features=AutomationControlled")
        Options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=Options)
        self.driver.get(start_url)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.current_page_iframes = []
        self.all_page_loaded()

        if not path.exists(self.PROJECT_PATH):
            os.makedirs(self.PROJECT_PATH)
        filename = self.title_to_class_name()
        code_filename = os.path.join(self.PROJECT_PATH, '.'.join([filename, 'py']))
        self.PY_FUNC_NAME_LIST = []
        self.code2file(
            code=self.identify_inputs_and_buttons(
                filename, self.driver.current_url, self.driver.page_source, elements, exclude_elements
            ),
            filename=code_filename,
        )
        if self.current_page_iframes:
            for index, frame in enumerate(self.current_page_iframes):
                self.driver.switch_to.frame(frame)
                self.code2file(
                    code=self.identify_inputs_and_buttons(
                        filename, self.driver.current_url, self.driver.page_source,
                        elements, exclude_elements,
                        iframe_index=index, is_iframe=True
                    ),
                    filename=code_filename,
                    mode="a",
                )
                self.driver.switch_to.default_content()
        self.PageUrls = {self.driver.current_url}
        self.PageHandles = self.driver.window_handles
        while True:
            sleep(0.2)
            self.all_page_loaded()
            try:
                cur_url = self.driver.current_url
                cur_handles = self.driver.window_handles
                if cur_url not in self.PageUrls:
                    self.PageUrls.add(cur_url)
                    filename = self.title_to_class_name()
                    code_filename = os.path.join(self.PROJECT_PATH, '.'.join([filename, 'py']))
                    self.PY_FUNC_NAME_LIST = []
                    self.code2file(
                        code=self.identify_inputs_and_buttons(
                            filename, self.driver.current_url, self.driver.page_source, elements, exclude_elements
                        ),
                        filename=code_filename,
                    )
                    if self.current_page_iframes:
                        for index, frame in enumerate(self.current_page_iframes):
                            self.driver.switch_to.frame(frame)
                            self.code2file(
                                code=self.identify_inputs_and_buttons(
                                    filename, self.driver.current_url, self.driver.page_source,
                                    elements, exclude_elements,
                                    iframe_index=index, is_iframe=True
                                ),
                                filename=code_filename,
                                mode="a",
                            )
                            self.driver.switch_to.default_content()
                if cur_handles != self.PageHandles:
                    for handle in cur_handles:
                        self.driver.switch_to.window(handle)
                        if self.driver.current_url not in self.PageUrls:
                            self.PageUrls.add(self.driver.current_url)
                            filename = self.title_to_class_name()
                            code_filename = os.path.join(self.PROJECT_PATH, '.'.join([filename, 'py']))
                            self.PY_FUNC_NAME_LIST = []
                            self.code2file(
                                code=self.identify_inputs_and_buttons(
                                    filename, self.driver.current_url, self.driver.page_source,
                                    elements, exclude_elements
                                ),
                                filename=code_filename,
                            )
                            if self.current_page_iframes:
                                for index, frame in enumerate(self.current_page_iframes):
                                    self.driver.switch_to.frame(frame)
                                    self.code2file(
                                        code=self.identify_inputs_and_buttons(
                                            filename, self.driver.current_url, self.driver.page_source,
                                            elements, exclude_elements,
                                            iframe_index=index, is_iframe=True
                                        ),
                                        filename=code_filename,
                                        mode="a",
                                    )
                                    self.driver.switch_to.default_content()
                    self.PageHandles = self.driver.window_handles
            except KeyboardInterrupt as e:
                exit(0)
            except NoSuchWindowException as e:
                exit(-1)

    def all_page_loaded(self):
        # 主页面加载完毕
        while self.driver.execute_script("return document.readyState;") != "complete":
            sleep(0.1)
        try:
            # 内嵌页面加载完毕
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
        except Exception as e:
            pass
        finally:
            # 获取所有 iframe 元素
            self.current_page_iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        # 遍历所有 iframe
        if self.current_page_iframes:
            for iframe in self.current_page_iframes:
                try:
                    self.driver.switch_to.frame(iframe)  # 切换到 iframe
                    WebDriverWait(self.driver, 30).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                except Exception as e:
                    pass
                finally:
                    # 这里可以进行需要的操作
                    self.driver.switch_to.default_content()  # 切换回主页面

    def code2file(self, code: str, filename: str = None, mode="w", encoding="UTF-8"):
        with open(filename, mode=mode, encoding=encoding) as f:
            f.write(code)
            f.close()
            del f

    def identify_inputs_and_buttons(self, class_name='', url='', html='',
                                    elements=None, exclude_elements=None,
                                    iframe_index=0, is_iframe=False):
        soup = BeautifulSoup(html, "html.parser")
        find_all_input = []
        find_all_button = []
        exclude_elements_list = [] if exclude_elements.split(',') in [[], ['']] else exclude_elements.split(',')
        if elements == '*': # html的所有标签
            include_elements_list = [x.name for x in soup.find_all()]
        else:
            include_elements_list = [] if elements.split(',') in [[], ['']] else elements.split(',')
        if 'textarea' not in exclude_elements_list and 'textarea' in include_elements_list:
            find_all_input.extend(soup.find_all("textarea"))
        if 'input' not in exclude_elements_list and 'input' in include_elements_list:
            find_all_input.extend(
                soup.find_all("input",
                              attrs={"type": ["text", "password", "number", "email", "tel", "url", "search"]}))
            find_all_button.extend(
                soup.find_all("input",
                              attrs={"type": ["button", "submit", "checkbox", "radio", "file", "hidden"]})
            )
        if elements:
            exclude_elements_list.extend(["", "input", "textarea"])
            elements_list = [x for x in include_elements_list if x not in exclude_elements_list]
            if elements_list:
                for element in elements_list:
                    find_all_button.extend(soup.find_all(element))
        if is_iframe:
            return self.iframe_converter(
                iframe_index=iframe_index, input_list=find_all_input, button_list=find_all_button
            )
        return self.converter(
            class_name=class_name, url=url, input_list=find_all_input, button_list=find_all_button
        )

    def get_xpath(self, element):
        components = []
        child = element
        while child is not None:
            siblings = child.find_previous_siblings()
            index = len(siblings) + 1
            if child.name == "html":
                components.insert(0, "/html")
                break
            if child.name == "body":
                components.insert(0, "/body")
                break
            else:
                element_attrs_dict = child.attrs
                for k, v in element_attrs_dict.items():
                    if k in element_attrs_dict.keys() and "" != element_attrs_dict[k]:
                        html = etree.HTML(self.driver.page_source)
                        query_result = html.xpath(
                            f'//{child.name}[@{k}="{element_attrs_dict[k]}"]'
                        )
                        if len(query_result) == 1:
                            components.insert(
                                0, f'/{child.name}[@{k}="{element_attrs_dict[k]}"]'
                            )
                            xpath = "".join(components)
                            xpath = xpath if xpath.startswith("/html") else "/" + xpath
                            xpath = xpath.replace("'", "\\'")
                            return xpath
                        else:
                            continue
            components.insert(0, f"/{child.name}[{index}]")
            child = child.parent
        xpath = "".join(components)
        xpath = xpath if xpath.startswith("/html") else "/" + xpath
        xpath = xpath.replace("'", "\\'")
        return xpath

    def title_to_class_name(self):
        _title_ = "".join(re.findall(r"\w+", self.driver.title))
        class_name = "_".join(lazy_pinyin(_title_)).title()
        if len(class_name) > 10:
            class_name = ''.join([x[0] for x in class_name.split('_') if len(x) > 0])
            class_name = class_name[:10]
        if not class_name:
            if 'FILE_COUNT' not in os.environ.keys():
                os.environ['FILE_COUNT'] = '0'
            else:
                os.environ['FILE_COUNT'] = str(int(os.environ['FILE_COUNT']) + 1)
            class_name = f'FILE_{os.environ["FILE_COUNT"]}'
        self.PY_FILE_NAME_LIST.append(class_name)
        if self.PY_FILE_NAME_LIST.count(class_name) > 1:
            class_name = f'{class_name}_{self.PY_FILE_NAME_LIST.count(class_name) - 1}'

        return class_name


    def element_to_func_name(self, element):
        try:
            func_name = element.get("name") or element.get("id") or element.text or element.get("class")[0] or element.name
        except Exception as e:
            func_name = element.name
        function_name = "_".join(lazy_pinyin(func_name))
        function_name = "".join(re.findall("[a-zA-Z_]+", function_name))
        if len(function_name) > 10:
            function_name = ''.join([x[0] for x in function_name.split('_') if len(x) > 0])
            function_name = function_name[:10]
        self.PY_FUNC_NAME_LIST.append(function_name)
        if self.PY_FUNC_NAME_LIST.count(function_name) > 1:
            function_name = f'{function_name}_{self.PY_FUNC_NAME_LIST.count(function_name) - 1}'
        return function_name

    def converter(self, class_name: str, url: str, input_list: list, button_list: list):
        function_strings = []
        function_strings.append("#! /usr/bin/env python")
        function_strings.append("# -*- coding: utf-8 -*-")
        function_strings.append(f"")
        function_strings.append("from selenium.webdriver.common.by import By")
        function_strings.append(f"")
        function_strings.append(f"class {class_name}(object):")
        function_strings.append("\tdef __init__(self, driver):")
        function_strings.append(f"\t\tself.page_url = '{url}'")
        function_strings.append("\t\tself.driver = driver")
        function_strings.append("\t\tself.page_iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')")
        function_strings.append(f"")
        for input_item in input_list:
            function_name = self.get_func_name(input_item)
            xpath = self.get_xpath(input_item)
            function_strings.append(f"\tdef send_{function_name}(self, data):")
            function_strings.append("\t\t'''")
            function_strings.append("\t\t当前元素：")
            input_item_str = str(input_item).replace("\n", "\n\t\t")
            function_strings.append(f"\t\t{input_item_str}")
            function_strings.append("\t\t'''")
            function_strings.append(f"\t\tself.driver.find_element(By.XPATH, '{xpath}').send_keys(data)")
            function_strings.append(f"")
        for button_item in button_list:
            function_name = self.get_func_name(button_item)
            xpath = self.get_xpath(button_item)
            function_strings.append(f"\tdef click_{function_name}(self):")
            function_strings.append("\t\t'''")
            function_strings.append("\t\t当前元素：")
            button_item_str = str(button_item).replace("\n", "\n\t\t")
            function_strings.append(f"\t\t{button_item_str}")
            function_strings.append("\t\t'''")
            function_strings.append(f"\t\tself.driver.find_element(By.XPATH, '{xpath}').click()")
            function_strings.append(f"")
        return "\n".join(function_strings)

    def iframe_converter(self, iframe_index=0, input_list: list = None, button_list: list = None):
        function_strings = []
        function_strings.append(f"")
        for input_item in input_list:
            function_name = self.get_func_name(input_item)
            xpath = self.get_xpath(input_item)
            function_strings.append(f"\tdef send_{function_name}(self, data):")
            function_strings.append("\t\t'''")
            function_strings.append("\t\t当前元素：")
            input_item_str = str(input_item).replace("\n", "\n\t\t")
            function_strings.append(f"\t\t{input_item_str}")
            function_strings.append("\t\t'''")
            function_strings.append(f"\t\tself.driver.switch_to.frame(self.current_page_iframes[{iframe_index}])")
            function_strings.append(f"\t\tself.driver.find_element(By.XPATH, '{xpath}').send_keys(data)")
            function_strings.append(f"\t\tself.driver.switch_to.default_content()")
            function_strings.append(f"")
        for button_item in button_list:
            function_name = self.get_func_name(button_item)
            xpath = self.get_xpath(button_item)
            function_strings.append(f"\tdef click_{function_name}(self):")
            function_strings.append("\t\t'''")
            function_strings.append("\t\t当前元素：")
            button_item_str = str(button_item).replace("\n", "\n\t\t")
            function_strings.append(f"\t\t{button_item_str}")
            function_strings.append("\t\t'''")
            function_strings.append(f"\t\tself.driver.switch_to.frame(self.current_page_iframes[{iframe_index}])")
            function_strings.append(f"\t\tself.driver.find_element(By.XPATH, '{xpath}').click()")
            function_strings.append(f"\t\tself.driver.switch_to.default_content()")
            function_strings.append(f"")
        return "\n".join(function_strings)

def main():
    __pom_version__ = '.'.join(map(str, (0, 2)))
    parser = ArgumentParser(
        description="基于Selenium基础操作过程中将每页内容转为POM代码·v" + __pom_version__,
        epilog="全参示例：xiaobaipom --url https://www.baidu.com --dir . --elements image,iframe --exclude_elements span,div --rewrite",
    )
    parser.add_argument('-u', '--url', type=str, help='首页URL地址', default='https://www.baidu.com')
    parser.add_argument('-d', '--dir', type=str, help='代码输出目录', default='pageObjects')
    parser.add_argument('-r', '--rewrite', type=bool, help='是否覆盖旧文件', default=True)
    parser.add_argument('-e', '--elements', type=str,
                        help='自定义需要定位的元素，写法例如：image 或者 image,iframe 或者 *（*表示全部标签）',
                        default='a,input,button')
    parser.add_argument('-x', '--exclude_elements', type=str,
                        help='自定义需要排除的元素，写法例如：image 或者 image,iframe',
                        default='')
    args = parser.parse_args()
    PageListener(start_url=args.url, dirname=args.dir, rewrite=args.rewrite, elements=args.elements,
                 exclude_elements=args.exclude_elements)

if __name__ == '__main__':
    main()
