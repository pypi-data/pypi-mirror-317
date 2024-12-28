#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/23 19:36
fileName    : add_ui.py
'''

#  UI
from tkinter.filedialog import askopenfilename
from tkinter import *

# 工具
import os
import re
import traceback
import subprocess
import platform
from urllib.parse import urlparse
from api_project.common.LOG import Logger
from api_project.common.ENV import ENV
from api_project.common.CSV import Writer
from api_project import (
    CASE_CONFIG_PATH, CASE_SCRIPT_DIR_PATH,
    CASE_DATA_DIR_PATH, FEED, CONFIG_DIR_PATH,
    FAVICON_PATH, ALLURE_BIN_PATH
)
from api_project import TAB_SPACE
from saf.utils.Curl2Object import Curl, Template

__version__ = '.'.join(map(str, (0,  1, 1)))

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.file_path = StringVar()
        self.file_path.set('请选择待转换的cURL文件...（必填项）')
        self.tk_input_file_path = self.__tk_input_file_path(self)
        self.tk_button_choose_file_button = self.__tk_button_choose_file_button(self)
        self.tk_button_start_button = self.__tk_button_start_button(self)
        self.tk_text_log = self.__tk_text_log(self)
        self.tk_label_url_prefix_label = self.__tk_label_url_prefix_label(self)
        self.url_prefix = StringVar()
        self.url_prefix.set('请输入接口地址的前缀...（必填项）')
        self.tk_input_url_prefix_input = self.__tk_input_url_prefix_input(self)
        self.tk_label_choose_allure_path_label = self.__tk_label_choose_allure_path_label(self)
        self.allure_path = StringVar()
        self.allure_path.set('双击或者右击选择Allure路径（必填项）')
        self.tk_input_choose_allure_path_input = self.__tk_input_choose_allure_path_input(self)
        self.tk_label_frame_radio_frame = self.__tk_label_frame_radio_frame(self)
        self.radio_value = IntVar()
        self.radio_value.set(1)
        self.tk_radio_button_choose_ptest_allure_radio = self.__tk_radio_button_choose_ptest_allure_radio(
            self.tk_label_frame_radio_frame)
        self.tk_radio_button_choose_ptest_allure_at_radio = self.__tk_radio_button_choose_ptest_allure_at_radio(
            self.tk_label_frame_radio_frame)

    def __win(self):
        self.title("cURL2PyCode v" + __version__)
        self.iconbitmap(FAVICON_PATH)

        # 设置窗口大小、居中
        width = 400
        height = 370
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    def scrollbar_autohide(self, vbar, hbar, widget):
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

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_input_file_path(self, parent):
        ipt = Entry(parent, textvariable=self.file_path)
        ipt.place(relx=0.0500, rely=0.0270, relwidth=0.7025, relheight=0.0811)

        return ipt

    def __tk_button_choose_file_button(self, parent):
        btn = Button(parent, text="选择文件...", takefocus=False, bg='lightgreen')
        btn.place(relx=0.7750, rely=0.0270, relwidth=0.1725, relheight=0.0811)
        return btn

    def __tk_button_start_button(self, parent):
        btn = Button(parent, text="开 始 转", takefocus=False, bg='lightgreen')
        btn.place(relx=0.5525, rely=0.4324, relwidth=0.3925, relheight=0.2243)
        return btn

    def __tk_text_log(self, parent):
        text = Text(parent)
        text.place(relx=0.0000, rely=0.7297, relwidth=1.0000, relheight=0.2703)
        self.create_bar(parent, text, True, True, 0, 270, 400, 100, 400, 370)
        return text

    def __tk_label_url_prefix_label(self, parent):
        label = Label(parent, text="*URL前缀：", anchor="center", )
        label.place(relx=0.0500, rely=0.1541, relwidth=0.1625, relheight=0.0811)
        return label

    def __tk_input_url_prefix_input(self, parent):
        ipt = Entry(parent, textvariable=self.url_prefix)
        ipt.place(relx=0.2125, rely=0.1541, relwidth=0.7325, relheight=0.0811)
        return ipt

    def __tk_label_choose_allure_path_label(self, parent):
        label = Label(parent, text="*Allure：", anchor="center", )
        label.place(relx=0.0500, rely=0.2811, relwidth=0.1625, relheight=0.0811)
        return label

    def __tk_input_choose_allure_path_input(self, parent):
        ipt = Entry(parent, textvariable=self.allure_path)
        ipt.place(relx=0.2150, rely=0.2811, relwidth=0.7325, relheight=0.0811)
        return ipt

    def __tk_label_frame_radio_frame(self, parent):
        frame = LabelFrame(parent, text="模板选择", )
        frame.place(relx=0.0500, rely=0.3919, relwidth=0.4400, relheight=0.3000)
        return frame

    def __tk_radio_button_choose_ptest_allure_radio(self, parent):
        rb = Radiobutton(parent, text="pytest_allure", value=1, variable=self.radio_value)
        rb.place(relx=0.1136, rely=0.0180, relwidth=0.7614, relheight=0.2703)
        return rb

    def __tk_radio_button_choose_ptest_allure_at_radio(self, parent):
        rb = Radiobutton(parent, text="pytest_allure_at", value=2, variable=self.radio_value)
        rb.place(relx=0.1136, rely=0.4505, relwidth=0.7841, relheight=0.2703)
        return rb


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self, Logger())

    def __event_bind(self):
        self.tk_button_choose_file_button.bind('<Button-1>', self.ctl.choose_file)
        self.tk_button_start_button.bind('<Button-1>', self.ctl.run_convert)
        self.tk_text_log.bind('<Delete>', self.ctl.clear_log)
        self.tk_input_choose_allure_path_input.bind('<Button-3>', self.ctl.choose_allure_path)
        self.tk_input_choose_allure_path_input.bind('<Double-Button-1>', self.ctl.choose_allure_path)
        pass

    def __style_config(self):
        pass

class Controller:
    ui: Win
    logger: Logger
    def __init__(self):
        pass

    def init(self, ui, logger):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        self.logger = logger
        self.find_allure_path()

    def get_url_prefix(self, file_path):
        ''' 正则获取全部URL的前缀中最多的一个 '''
        all_urls = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            f.close()
            for line in lines:
                if '-H' not in line or '--header' not in line:
                    match = re.search(r'http[^\'"\s]+|https[^\'"\s]+', line)
                    if match:
                        all_urls.append(match.group())
        # 统计每个链接的前缀次数
        url_counts = {}
        for url in all_urls:
            sp = urlparse(url).path
            if sp:
                prefix = url.split(sp)[0]
            else:
                prefix = url
            if prefix not in ['http', 'https', 'http:', 'https:', 'http://', 'https://']:
                if prefix in url_counts:
                    url_counts[prefix] += 1
                else:
                    url_counts[prefix] = 1
        max_count_url = max(url_counts, key=url_counts.get)
        if max_count_url:
            if max_count_url.endswith('/'):
                max_count_url = max_count_url[:-1]
            self.ui.url_prefix.set(max_count_url)

    def choose_file(self,evt):
        self.file_path = askopenfilename(initialdir='~/Desktop',
                                         title='打开cURL命令文件',
                                         filetypes=[('All Files', '*.*')])
        if self.file_path:
            self.ui.file_path.set(self.file_path)
            self.ui.tk_text_log.insert('end', f"您选择的文件是：{self.file_path}\n")
            self.logger.info(f"您选择的文件是：{self.file_path}")
            # 读取文件内容获取所有url的前缀
            self.get_url_prefix(self.file_path)
        else:
            self.ui.tk_text_log.insert('end', "您取消的选择\n")
            self.logger.info("您取消的选择")

    def run_convert(self,evt):
        ENV.load()
        file_path = self.ui.file_path.get()
        if  file_path not in ['',  '请选择待转换的cURL文件...（必填项）']:
            if self.ui.url_prefix.get() in ['', '请输入接口地址的前缀...（必填项）']:
                self.ui.tk_text_log.insert('end', '接口地址的前缀是必填项，不能为空！\n')
                self.logger.error('接口地址的前缀是必填项，不能为空！')

                return
            else:
                # 重写host_config.py
                code = f'{FEED}'.join([
                    "#! /usr/bin/env python",
                    "'''",
                    "Auther      : xiaobaiTser",
                    "Email       : 807447312@qq.com",
                    "createTime  : 2024/11/21 19:24",
                    "fileName    : host_config.py",
                    "'''",
                    "",
                    "class HOST(object):",
                    f"{TAB_SPACE}TEST_HOST: str = '{self.ui.url_prefix.get()}'",
                    f"{TAB_SPACE}PRO_HOST: str = '{self.ui.url_prefix.get()}'",
                    f"{TAB_SPACE}CURRENT_HOST: str = TEST_HOST",
                ])
                with open(os.path.join(CONFIG_DIR_PATH, 'host_config.py'), 'w', encoding='utf-8') as f:
                    f.write(code)
                    f.close()
                self.ui.tk_text_log.insert('end', '已经重写host_config.py\n')
                self.logger.info('已经重写host_config.py')
                os.environ['HOST'] = self.ui.url_prefix.get()

            if self.ui.allure_path.get() not in ['', '双击或者右击选择Allure路径（必填项）']:
                # 重写allure_config.py
                code = f'{FEED}'.join([
                    "#! /usr/bin/env python",
                    "'''",
                    "Auther      : xiaobaiTser",
                    "Email       : 807447312@qq.com",
                    "createTime  : 2024/11/25 10:51",
                    "fileName    : allure_config.py",
                    "'''",
                    "",
                    "from ..common.Network import get_local_ip #, get_ip",
                    "",
                    "class Allure(object):",
                    f"{TAB_SPACE}PATH    : str = r'{self.ui.allure_path.get()}'",
                    f"{TAB_SPACE}IP      : str = get_local_ip()",
                    f"{TAB_SPACE}PORT    : int = 9797",
                ])
                with open(os.path.join(CONFIG_DIR_PATH, 'allure_config.py'), 'w', encoding='utf-8') as f:
                    f.write(code)
                    f.close()
                self.ui.tk_text_log.insert('end', '已经重写allure_config.py\n')
                self.logger.info('已经重写allure_config.py')

            self.ui.tk_text_log.insert('end', '已经加载环境变量\n')
            self.logger.info('已经加载环境变量')
            curl = Curl()
            curl.load(curl_file_path=file_path)
            self.ui.tk_text_log.insert('end', f'已加载文件[{os.path.split(file_path)[1]}]，正在进行转换\n')
            self.logger.info(f'已加载文件[{os.path.split(file_path)[1]}]，正在进行转换')
            for request in curl.group:
                # 获取接口名称：
                API_NAME = request.get('api_name')
                if 'api_name' in request.keys(): del request['api_name']
                newline = f"{API_NAME}_CASE_DATA_PATH = os.path.join(CASE_DATA_DIR_PATH, '{API_NAME}.csv'){FEED}"
                try:
                    with open(CASE_CONFIG_PATH, 'r', encoding='utf-8') as fr:
                        alllines = fr.readlines()
                        if newline not in alllines:
                            # 写入测试用例数据路径
                            with open(CASE_CONFIG_PATH, 'a', encoding='utf-8') as fa:
                                fa.write(f"{newline}")
                                fa.close()
                            self.ui.tk_text_log.insert('end', f"{os.path.split(CASE_CONFIG_PATH)[1]} 写入{newline}成功！\n")
                            self.logger.info(f"{os.path.split(CASE_CONFIG_PATH)[1]} 写入{newline}成功！")
                        del alllines
                        fr.close()
                except Exception as e:
                    self.ui.tk_text_log.insert('end', f"{os.path.split(CASE_CONFIG_PATH)[1]} 写入{newline}失败：{traceback.format_exc()}\n")
                    self.logger.error(f"{os.path.split(CASE_CONFIG_PATH)[1]} 写入{newline}失败：{traceback.format_exc()}")

                # 写入测试用例脚本
                CASE_SCRIPT = os.path.join(CASE_SCRIPT_DIR_PATH, f"test_{API_NAME.lower()}.py")
                try:
                    with open(CASE_SCRIPT, 'w', encoding='utf-8') as fw:
                        if self.ui.radio_value.get() == 1:
                            fw.write(Template.requests_pytest_allure_template(api_name=API_NAME, request=request))
                        else:
                            fw.write(Template.requests_pytest_allure_template_at(api_name=API_NAME, request=request))
                        fw.close()
                    self.ui.tk_text_log.insert('end', f"test_{API_NAME.lower()}.py 写入成功！\n")
                    self.logger.info(f"test_{API_NAME.lower()}.py 写入成功！")
                except Exception as e:
                    self.ui.tk_text_log.insert('end', f"test_{API_NAME.lower()}.py 写入失败：{traceback.format_exc()}\n")
                    self.logger.error(f"test_{API_NAME.lower()}.py 写入失败：{traceback.format_exc()}")

                # 写入测试用例数据文件
                CASE_DATA = os.path.join(CASE_DATA_DIR_PATH, f"{API_NAME}.csv")
                if not os.path.isdir(CASE_DATA_DIR_PATH):
                    os.mkdir(CASE_DATA_DIR_PATH)
                try:
                    if os.path.isfile(CASE_DATA):
                        Writer(file_path=CASE_DATA,
                               data=[list(request.keys()), list(request.values())],
                               ignore_first_row=True)
                    else:
                        Writer(file_path=CASE_DATA,
                               data=[list(request.keys()), list(request.values())],
                               ignore_first_row=False)
                    self.ui.tk_text_log.insert('end', f"{API_NAME}.csv 写入成功！\n")
                    self.logger.info(f"{API_NAME}.csv 写入成功！")
                except Exception as e:
                    self.ui.tk_text_log.insert('end', f"{API_NAME}.csv 写入失败：{traceback.format_exc()}\n")
                    self.logger.error(f"{API_NAME}.csv 写入失败：{traceback.format_exc()}")
        else:
            self.ui.tk_text_log.insert('end', '还未选择需要转换的文件\n')
            self.logger.error('还未选择需要转换的文件')

    def clear_log(self,evt):
        self.ui.tk_text_log.delete('1.0', END)

    def find_allure_path(self):
        if ALLURE_BIN_PATH:
            self.ui.allure_path.set(ALLURE_BIN_PATH)
        else:
            system = platform.system()
            if system == "Windows":
                try:
                    result = subprocess.run(["where", "allure.bat"], capture_output=True, text=True, check=True)
                    paths  = result.stdout.strip().split("\n")
                    self.ui.allure_path.set(list(filter(lambda x: str(x).endswith('allure.bat'), paths))[0])
                except subprocess.CalledProcessError:
                    pass
            elif system in ["Linux", "Darwin"]:
                try:
                    result = subprocess.run(["which", "allure"], capture_output=True, text=True, check=True)
                    paths  = [result.stdout.strip()]
                    self.ui.allure_path.set(list(filter(lambda x: str(x).endswith('allure'), paths))[0])
                except subprocess.CalledProcessError:
                    pass
            else:
                pass

    def choose_allure_path(self, evt):
        file_path = askopenfilename(initialdir='~/Desktop',
                                         title='打开Allure文件',
                                         filetypes=[('All Files', '*.*')])
        if file_path:
            self.ui.allure_path.set(file_path)

if __name__ == "__main__":
    try:
        win = Win(Controller())
        win.mainloop()
    except KeyboardInterrupt as e:
        pass