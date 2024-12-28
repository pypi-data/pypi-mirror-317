#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2024/8/14 23:52
@File  : MonitorCP.py
'''
import os
import re
import time
from urllib.parse import urlparse
from tkinter import messagebox, filedialog

from ujson import dumps

import pyperclip
from tkinter import *
from tkinter.ttk import *
from threading import Thread

FAVICON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/favicon.ico")

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_button_monitor_button = self.__tk_button_monitor_button(self)
        self.tk_button_copy_button = self.__tk_button_copy_button(self)
        self.tk_text_code_text = self.__tk_text_code_text(self)
        self.tk_select_box_type_box = self.__tk_select_box_type_box(self)
        self.monitor_status = False
        self.SourceData = None
        self.GenerateCodeStatus = False
    def __win(self):
        self.title("小白代码转换器")
        self.iconbitmap(FAVICON_PATH)
        # 设置窗口大小、居中
        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_button_monitor_button(self,parent):
        btn = Button(parent, text="开  始", takefocus=False,)
        btn.place(relx=0.0000, rely=0.0000, relwidth=0.1300, relheight=0.0680)
        return btn
    def __tk_button_copy_button(self,parent):
        btn = Button(parent, text="复 制", takefocus=False, )
        btn.place(relx=0.8650, rely=0.0000, relwidth=0.1317, relheight=0.0680)
        # 禁用
        btn.state=DISABLED
        return btn
    def __tk_text_code_text(self,parent):
        text = Text(parent)
        text.place(relx=0.0000, rely=0.0640, relwidth=1.0000, relheight=0.9320)
        text.see(END)
        self.create_bar(parent, text,True, True, 0, 32, 600,466,600,500)
        return text
    def __tk_select_box_type_box(self,parent):
        cb = Combobox(parent, state="readonly")
        cb['values'] = ("fetch(nodejs)2requests(base)",
                        "fetch(nodejs)2requests(pytest)",
                        "fetch(nodejs)2requests(pytest_allure)",
                        )
        cb.current(0)
        cb.place(relx=0.2900, rely=0.0000, relwidth=0.4000, relheight=0.0650)
        return cb
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_monitor_button.bind('<Button>',self.ctl.start_monitor)
        self.tk_select_box_type_box.bind('<<ComboboxSelected>>',self.ctl.monitor_select_box_change)
        self.tk_button_copy_button.bind('<Button>',self.ctl.copy_code_text)
        self.tk_text_code_text.bind('<Double-Button-1>',self.ctl.copy_code_text)
        # 监听快捷键 Ctrl + s
        self.bind('<Control-s>',self.ctl.save_code)
        pass
    def __style_config(self):
        pass

class RequestCodeTemplate:
    def __init__(self, url, method, headers, body, ui, first=False):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.ui = ui
        self.first = first

    def __type__(self):
        return self.ui.tk_select_box_type_box.get()

    def getCode(self):
        if self.__type__() == 'fetch(nodejs)2requests(base)':
            return self.ToRequestsOfBaseHeader() + self.ToRequestsOfBaseRequest() if self.first \
                else self.ToRequestsOfBaseRequest()
        elif self.__type__() == 'fetch(nodejs)2requests(pytest)':
            return self.ToRequestsOfPytestHeader() + self.ToRequestsOfPytestRequest() if self.first \
                else self.ToRequestsOfPytestRequest()
        elif self.__type__() == 'fetch(nodejs)2requests(pytest_allure)':
            return self.ToRequestsOfPytestAllureHeader() + self.ToRequestsOfPytestAllureRequest() if self.first \
                else self.ToRequestsOfPytestAllureRequest()

    def ToRequestsOfBaseHeader(self):
        return f'''#! /usr/bin/env python
##################################
#       requests(Base)           #
#       author: xiaobaiTser      #
#       email : 807447312@qq.com #
##################################
from requests import request

'''

    def ToRequestsOfBaseRequest(self):
        _path = urlparse(self.url).path
        func_name_fix = _path.split('/')[-1] if _path not in ['', '/'] else 'index'
        func_name_fix = re.sub(r'\W', '_', func_name_fix)
        return f'''
##############{func_name_fix}################
url = '{self.url}'
method = '{self.method}'
headers = {dumps(self.headers, indent=4)}
body = '{self.body}'
response = request(method=method, url=url, headers=headers, data=body, verify=False)

# 断言
assert response.status_code == 200
# assert response.json()['msg'] == "请求成功"
'''

    def ToRequestsOfPytestHeader(self):
        return f'''#! /usr/bin/env python
##################################
#       requests(PyTest)         #
#       author: xiaobaiTser      #
#       email : 807447312@qq.com #
##################################
from requests import request
import pytest

'''

    def ToRequestsOfPytestRequest(self):
        _path = urlparse(self.url).path
        func_name_fix = _path.split('/')[-1] if _path not in ['', '/'] else 'index'
        func_name_fix = re.sub(r'\W', '_', func_name_fix)
        return f'''
@pytest.mark.{func_name_fix}
def test_{func_name_fix}():
    url = '{self.url}'
    method = '{self.method}'
    headers = {dumps(self.headers, indent=8)}
    body = '{self.body}'
    response = request(method=method, url=url, headers=headers, data=body, verify=False)
    
    # 断言
    assert response.status_code == 200
    # assert response.json()['msg'] == "成功"
'''

    def ToRequestsOfPytestAllureHeader(self):
        return f'''#! /usr/bin/env python
##################################
#       requests(PyTest_Allure)  #
#       author: xiaobaiTser      #
#       email : 807447312@qq.com #
##################################
from requests import request
import pytest
import allure

'''

    def ToRequestsOfPytestAllureRequest(self):
        _path = urlparse(self.url).path
        func_name_fix = _path.split('/')[-1] if _path not in ['', '/'] else 'index'
        func_name_fix = re.sub(r'\W', '_', func_name_fix)
        return f'''
@allure.story('{func_name_fix}')
def test_{func_name_fix}():
    #with allure.step('数据准备'):
    url = '{self.url}'
    method = '{self.method}'
    headers = {dumps(self.headers, indent=8)}
    body = '{self.body}'
    #with allure.step('接口发起请求'):
    response = request(method=method, url=url, headers=headers, data=body, verify=False)

    #with allure.step('断言')
    assert response.status_code == 200
    # assert response.json()['msg'] == "成功"
'''

def convert_to_code(source, ui):
    if ui.tk_select_box_type_box.get().startswith('fetch'):
        source = source.replace('null', '\'\'')
        if '; ;\r\nfetch' in source:
            fetch_all = source.split('; ;\r\nfetch')  # 除第一个之外
            for fetch in fetch_all:
                if fetch.startswith('fetch(') and \
                        '"headers": {' in fetch and \
                        '"body":' in fetch and \
                        '"method":' in fetch and \
                        fetch.endswith('})'):
                    fetch_tuple = eval(fetch[5:])
                    url_text = fetch_tuple[0]
                    method_text = fetch_tuple[1]['method']
                    headers_dict = fetch_tuple[1]['headers']
                    body_text = fetch_tuple[1]['body']
                    code_text = RequestCodeTemplate(url_text, method_text, headers_dict, body_text, ui, first=True).getCode()
                    ui.tk_text_code_text.delete(1.0, END)
                    ui.tk_text_code_text.insert(END, code_text)
                    if ui.tk_button_copy_button.state == DISABLED:
                        ui.tk_button_copy_button.state = NORMAL
                elif not fetch.startswith('fetch(') and \
                        '"headers": {' in fetch and \
                        '"body":' in fetch and \
                        '"method":' in fetch and \
                        fetch.endswith('})'):
                    fetch_tuple = eval(fetch)
                    url_text = fetch_tuple[0]
                    method_text = fetch_tuple[1]['method']
                    headers_dict = fetch_tuple[1]['headers']
                    body_text = fetch_tuple[1]['body']
                    code_text = RequestCodeTemplate(url_text, method_text, headers_dict, body_text, ui, first=False).getCode()
                    ui.tk_text_code_text.insert(END, code_text)
                    if ui.tk_button_copy_button.state == DISABLED:
                        ui.tk_button_copy_button.state = NORMAL
        elif source.startswith('fetch(') and \
                        '"headers": {' in source and \
                        '"body":' in source and \
                        '"method":' in source and \
                        source.endswith('});'):
            fetch_tuple = eval(source[5:-1])
            url_text = fetch_tuple[0]
            method_text = fetch_tuple[1]['method']
            headers_dict = fetch_tuple[1]['headers']
            body_text = fetch_tuple[1]['body']
            code_text = RequestCodeTemplate(url_text, method_text, headers_dict, body_text, ui, first=True).getCode()
            ui.tk_text_code_text.delete(1.0, END)
            ui.tk_text_code_text.insert(END, code_text)
            if ui.tk_button_copy_button.state == DISABLED:
                ui.tk_button_copy_button.state = NORMAL
    elif ui.tk_select_box_type_box.get().startswith('curl'):
        pass
    ui.GenerateCodeStatus = True

# 子线程监控粘贴板
def monitor_clipboard_thread(ui):
    i = 0
    while ui.monitor_status:
        title = "小白代码转换器" + " · 正在监听粘贴板." + '.' * (i % 3)
        i += 1
        ui.title(title)
        if pyperclip.paste().startswith('fetch(') and \
                '"headers": {' in pyperclip.paste() and \
                '"body":' in pyperclip.paste() and \
                '"method":' in pyperclip.paste() and \
                pyperclip.paste().endswith('});'):
            convert_to_code(pyperclip.paste(), ui)
            ui.SourceData = pyperclip.paste()
            pyperclip.copy('')
        time.sleep(1)

# 控制
class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win
    def __init__(self):
        pass
    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作
    def start_monitor(self,evt):
        if self.ui.tk_button_monitor_button['text'] == '开  始':
            self.ui.monitor_status = True
            self.ui.tk_button_monitor_button['text'] = '停  止'
            self.st = Thread(target=monitor_clipboard_thread, args=(self.ui,))
            self.st.setDaemon(True)
            self.st.start()
        else:
            self.ui.monitor_status = False
            self.ui.GenerateCodeStatus = False
            self.ui.SourceData = None
            self.ui.tk_button_monitor_button['text'] = '开  始'
            self.ui.title("小白代码转换器")

    def monitor_select_box_change(self, evt):
        if self.ui.GenerateCodeStatus and self.ui.SourceData:
            convert_to_code(self.ui.SourceData, self.ui)

    def save_code(self, evt):
        if self.ui.tk_text_code_text.get(1.0, END) != '\n':
            filename = filedialog.asksaveasfilename(
                initialdir='~/Desktop',
                filetypes=[('python', '*.py')],
                defaultextension='.py')
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.ui.tk_text_code_text.get(1.0, END))
                    f.close()
                messagebox.showinfo('提示', '保存成功 😀')
        else:
            messagebox.showerror('错误:', '无数据不能保存')

    def copy_code_text(self,evt):
        if self.ui.tk_button_copy_button.state == NORMAL and self.ui.tk_text_code_text.get(1.0, END):
            pyperclip.copy(self.ui.tk_text_code_text.get(1.0, END))
            messagebox.showinfo('提示', '代码已复制到粘贴板 😀')
        else:
            messagebox.showerror('错误', '请先获取代码')

# 主程序
def cpmain():
    controller = Controller()
    ui = Win(controller)
    ui.mainloop()

if __name__ == "__main__":
    cpmain()