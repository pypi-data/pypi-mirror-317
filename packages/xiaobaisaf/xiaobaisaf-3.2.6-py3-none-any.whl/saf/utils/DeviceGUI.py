import os
import re
import psutil
import subprocess
from threading import Thread
from time import sleep, time
from tkinter.filedialog import asksaveasfilename
from chardet import detect
from adbutils import adb
from tkinter import *
from tkinter.ttk import *
from lxml import etree
from PIL import Image, ImageTk

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
FAVICON_PATH = os.path.join(CUR_DIR, "../data/favicon.ico")

GREP = 'findstr' if os.name == 'nt' else 'grep'
PYTHON = 'python' if os.name == 'nt' else 'python3'
SLEEP = 'timeout /t' if os.name == 'nt' else 'sleep'
SLEEP_END = '/nobreak > NUL' if os.name == 'nt' else ''

UI_DUMP_FILE = os.path.expanduser('~/window_dump.xml')

GETTIMER = True
tree = object

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_canvas_phone_ui = self.__tk_canvas_phone_ui(self)
        self.tk_select_box_connect_list = self.__tk_select_box_connect_list(self)
        self.tk_button_connect_button = self.__tk_button_connect_button(self)
        self.tk_text_output_code_text = self.__tk_text_output_code_text(self)
        self.tk_button_appium_status_button = self.__tk_button_appium_status_button(self)
        self.tk_button_save_code_button = self.__tk_button_save_code_button(self)
        self.tk_text_appium_log_text = self.__tk_text_appium_log_text(self)
        self.tk_button_run_code_button = self.__tk_button_run_code_button(self)
        self.tk_text_system_log_text = self.__tk_text_system_log_text(self)
        self.tk_button_clear_system_log_button = self.__tk_button_clear_system_log_button(self)
        self.tk_check_button_run_console_button = self.__tk_check_button_run_console_button(self)
        self.tk_select_box_output_type_select_button = self.__tk_select_box_output_type_select_button(self)
        self.tk_label_output_type_label = self.__tk_label_output_type_label(self)

    def __win(self):
        self.title("小白·APPUI监控器")
        # 设置窗口大小、居中
        width = 800
        height = 600
        self.iconbitmap(FAVICON_PATH)
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

    def __tk_canvas_phone_ui(self, parent):
        canvas = Canvas(parent, bg="#aaa")
        canvas.place(relx=0.0220, rely=0.0775, relwidth=0.2180, relheight=0.6438)
        return canvas

    def __tk_select_box_connect_list(self, parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("请选择设备...")
        cb.place(relx=0.0220, rely=0.0187, relwidth=0.1420, relheight=0.0375)
        return cb

    def __tk_button_connect_button(self, parent):
        btn = Button(parent, text="连  接", takefocus=False, )
        btn.place(relx=0.1800, rely=0.0187, relwidth=0.0590, relheight=0.0375)
        return btn

    def __tk_text_output_code_text(self, parent):
        text = Text(parent)
        text.see(END)
        text.place(relx=0.2600, rely=0.0788, relwidth=0.4180, relheight=0.6438)
        self.create_bar(parent, text, True, True, 260, 63, 418, 515, 1000, 800)
        return text

    def __tk_button_appium_status_button(self, parent):
        btn = Button(parent, text="启动APPium服务", takefocus=False, )
        btn.place(relx=0.7140, rely=0.0187, relwidth=0.1500, relheight=0.0375)
        return btn

    def __tk_button_save_code_button(self, parent):
        btn = Button(parent, text="保存脚本", takefocus=False, )
        btn.place(relx=0.5970, rely=0.0187, relwidth=0.0820, relheight=0.0375)
        return btn

    def __tk_text_appium_log_text(self, parent):
        text = Text(parent)
        text.see(END)
        text.place(relx=0.6990, rely=0.0775, relwidth=0.2800, relheight=0.6425)
        self.create_bar(parent, text, True, True, 699, 62, 280, 514, 1000, 800)
        return text

    def __tk_button_run_code_button(self, parent):
        btn = Button(parent, text="运行脚本", takefocus=False, )
        btn.place(relx=0.4710, rely=0.0187, relwidth=0.0920, relheight=0.0375)
        return btn

    def __tk_text_system_log_text(self, parent):
        text = Text(parent)
        text.see(END)
        text.place(relx=0.0210, rely=0.7475, relwidth=0.8580, relheight=0.2025)
        self.create_bar(parent, text, True, True, 21, 598, 858, 162, 1000, 800)
        return text

    def __tk_button_clear_system_log_button(self, parent):
        btn = Button(parent, text="清 除", takefocus=False, )
        btn.place(relx=0.9020, rely=0.7600, relwidth=0.0750, relheight=0.1762)
        return btn

    def __tk_check_button_run_console_button(self, parent):
        self.check_status = IntVar()
        self.check_status.set(0)
        cb = Checkbutton(parent, text="console", variable=self.check_status)
        cb.place(relx=0.8820, rely=0.0187, relwidth=0.0870, relheight=0.0375)
        return cb

    def __tk_select_box_output_type_select_button(self, parent):
        cb = Combobox(parent, state="readonly")
        cb['values'] = ("appium", "source", "adb")
        cb.place(relx=0.3400, rely=0.0187, relwidth=0.1000, relheight=0.0375)
        return cb

    def __tk_label_output_type_label(self, parent):
        label = Label(parent, text="输出类型：", anchor="center", )
        label.place(relx=0.2620, rely=0.0187, relwidth=0.0700, relheight=0.0375)
        return label
# 监控adb连接的设备

class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_select_box_connect_list.bind('<<ComboboxSelected>>', self.ctl.select_device)
        self.tk_button_connect_button.bind('<Button-1>', self.ctl.connect_device)
        self.tk_button_appium_status_button.bind('<Button-1>', self.ctl.start_stop_appium_service)
        self.tk_button_save_code_button.bind('<Button-1>', self.ctl.save_text_to_script)
        self.tk_button_run_code_button.bind('<Button-1>', self.ctl.run_code_text_script)
        self.tk_button_clear_system_log_button.bind('<Button-1>', self.ctl.clear_system_log)
        self.tk_check_button_run_console_button.bind('<Button-1>', self.ctl.change_console_status)
        self.tk_select_box_output_type_select_button.bind('<<ComboboxSelected>>', self.ctl._change_output_type)
    def __style_config(self):
        pass

class Controller:
    ui: Win
    current_device_x_min: int = 0
    current_device_x_max: int = 0
    current_device_y_min: int = 0
    current_device_y_max: int = 0
    output_type: str = 'appium'
    package_activity_list: dict = {}
    appium_service_process = None
    run_script_process = None
    current_device = None
    current_device_name: str = ''
    current_script_path: str = ''
    run_script_status: bool = False
    wait_kill_process_id_list: list = []
    def __init__(self):
        pass
    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        self.ui.tk_select_box_output_type_select_button.current(0)
        if self._monitor_appium_service_status():
            self.ui.tk_text_system_log_text.insert(END, 'Appium服务已启动\n')
            self.ui.tk_button_appium_status_button['text'] = '关闭Appium服务'
        else:
            self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
        Thread(target=self._monitor_connect_device_list_thread, daemon=True).start()

    def _change_output_type(self, _):
        self.output_type = self.ui.tk_select_box_output_type_select_button.get()
        self.ui.tk_text_system_log_text.insert(END, f'输出类型已切换为：{self.output_type}\n')

    def _monitor_appium_service_status(self):
        return False if not os.popen(f'netstat -an | {GREP} ":4723"').readlines() else True

    def _system_console_command_format(self, command):
        ''' 各系统终端执行命令的格式化 '''
        if os.name == 'nt':
            command = f'start cmd.exe /k {command}'
        elif os.name == 'posix':
            command = f'gnome-terminal -e \'bash -c "{command}; exec bash"\' '
        elif os.name == 'darwin':
            command = f'osascript -e "tell application "Terminal" to do script "{command}"'
        else:
            command = command
        return command

    def _kill_command_process(self, ppid: list = None):
        ''' 杀掉指定父进程id的所有子进程，支持windows、mac、linux '''
        # 遍历所有正在运行的进程
        for proc in psutil.process_iter(['pid', 'name', 'ppid']):
            if proc.info["ppid"] in ppid:
                self.wait_kill_process_id_list.append(proc.info["pid"])
                self._kill_command_process(ppid=[proc.info["pid"]])
        # 遍历所有正在运行的进程
        for pid in self.wait_kill_process_id_list[::-1]:
            try:
                psutil.Process(pid).terminate()
            except psutil.NoSuchProcess:
                pass

    def _quit_process(self, process: subprocess.Popen):
        ''' 退出子进程，支持windows、mac、linux '''
        self._kill_command_process(ppid=[process.pid])
        process.terminate()
        process.wait()

    def find_smallest_bounds_index(self, target, bounds_list):
        """
        查找包含目标点的最小边界的索引。

        参数：
            target (tuple): 目标点格式为 (x, y)。
            bounds_list (list): 边界列表，格式为 [[x0, y0, x1, y1], ...]。

        返回值：
            int: 包含目标点的最小边界的索引。
        """
        smallest_area = float('inf')
        smallest_index = 0

        for i, bounds in enumerate(bounds_list):
            x0, y0, x1, y1 = bounds
            if x0 < target[0] < x1 and y0 < target[1] < y1:
                area = (x1 - x0) * (y1 - y0)
                if area < smallest_area:
                    smallest_area = area
                    smallest_index = i
        return smallest_index

    def generate_xpath_with_attributes(self, element):
        # element 是xml文档中一个元素节点
        global tree
        if element is None:
            return ''
        if element.tag == 'hierarchy':
            class_value = element.get('class', '')
        else:
            class_value = element.get('class') if element.get('class') != '' else '*'
        resource_id = element.get('resource-id')
        text = element.get('text')

        if text and resource_id:
            return f'//{class_value}[@text="{text}" and @resource_id="{resource_id}"]'
        elif text:
            return f'//{class_value}[@text="{text}"]'
        elif resource_id:
            # 查询相同id的节点是否存在多个，多个返回点击坐标，只有一个则范围id的xpath表达式
            elements = tree.xpath(f'//*[@resource-id="{resource_id}"]')
            if len(elements) > 1:
                # 选出包含目标点的最小边界的索引
                # 点击元素的中心坐标
                element_bounds = [int(i) for i in re.findall(r'\d+', element.get('bounds'))]
                x = (element_bounds[0] + element_bounds[2]) / 2
                y = (element_bounds[1] + element_bounds[3]) / 2
                elements_bounds = [[int(i) for i in re.findall(r'\d+', element.get('bounds'))] for element in elements]
                index = self.find_smallest_bounds_index((x, y), elements_bounds)
                return f'//{class_value}[@resource-id="{resource_id}"][{index + 1}]'
            else:
                return f'//{class_value}[@resource_id="{resource_id}"]'
        else:
            parent = element.getparent()
            parent_xpath = self.generate_xpath_with_attributes(parent)
            return f'{parent_xpath}/{class_value}'

    def _monitor_timer_threader(self):
        global GETTIMER
        GETTIMER = True
        _start_time = time()
        while GETTIMER:
            pass
        if self.output_type == 'appium':
            self.ui.tk_text_output_code_text.insert(END, f'sleep({round(time() - _start_time, 1)})\n')
        elif self.output_type == 'source':
            sj = f"""\r\n\t\t{{\
                \r\n\t\t\t'action': 'wait',\
                \r\n\t\t\t'xpath': None,\
                \r\n\t\t\t'bounds': None,\
                \r\n\t\t\t'hold_time': {round(time() - _start_time, 1)}\
                \r\n\t\t}},\
                \r\n\t]\
                \r\n}}\n"""
            # 需要删除code_text的最后两行内容
            self.ui.tk_text_output_code_text.delete('end - 3 lines', 'end')
            self.ui.tk_text_output_code_text.insert(END, sj)
        else:
            self.ui.tk_text_output_code_text.insert(END, f'{SLEEP} {int(time() - _start_time)} {SLEEP_END}\n')

    def select_device(self, _):
        ''' 选择设备 '''
        self.current_device_name = self.ui.tk_select_box_connect_list.get()
        self.ui.tk_text_system_log_text.insert(END, f'设备[{self.current_device_name}]已选择\n')

    def connect_device(self, _):
        '''
        1、监控设备屏幕
        2、监控事件转为可运行代码或者事件数据
        '''
        if self.ui.tk_button_connect_button['text'] == '连  接':
            self.current_device = adb.device(self.current_device_name)
            try:
                Thread(target=self._monitor_device_screen_thread, daemon=True).start()
                Thread(target=self._monitor_device_event_thread, daemon=True).start()
                Thread(target=self._monitor_device_package_activity_thread, daemon=True).start()
                self.ui.tk_button_connect_button['text'] = '断  开'
                self.ui.tk_text_system_log_text.insert(END, f'设备[{self.current_device_name}]连接成功\n')
            except Exception as e:
                self.ui.tk_text_system_log_text.insert(END, f'设备[{self.current_device_name}]断开连接\n')
        else:
            self.ui.tk_button_connect_button['text'] = '连  接'
            self.ui.tk_text_system_log_text.insert(END, f'设备[{self.current_device.serial}]断开连接\n')
            self.current_device = None

    def start_stop_appium_service(self, _):
        '''
        监听4723端口是否被占用
        '''
        if self._monitor_appium_service_status():
            self.ui.tk_button_appium_status_button['text'] = '关闭Appium服务'
        else:
            self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
        if self.ui.tk_button_appium_status_button['text'] == '启动Appium服务':
            self.ui.tk_text_appium_log_text.delete(1.0, END)
            Thread(target=self._monitor_appium_service_thread, daemon=True).start()
        else:
            try:
                if self.appium_service_process and self.appium_service_process.poll() is None:
                    self._quit_process(self.appium_service_process)
                else:
                    # 删掉指定端口4723的APPIUM服务进程
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'ppid']):
                        if proc.info['cmdline'] and 'appium' in ' '.join(list(proc.info['cmdline'])):
                            self._quit_process(proc)
            except: pass
            self.ui.tk_text_appium_log_text.delete(1.0, END)
            self.ui.tk_text_system_log_text.insert(END, 'Appium服务已关闭\n')
            self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'

    def save_text_to_script(self, _):
        ''' 保存脚本 '''
        if self.output_type == 'appium':
            defaultextension = '.py'
        elif self.output_type == 'source':
            defaultextension = '.json'
        else:
            defaultextension = '.bat' if os.name == 'nt' else '.sh'
        self.current_script_path = asksaveasfilename(defaultextension=defaultextension,
                                      title='保存文件',
                                      initialdir=os.path.expanduser('~\\Desktop'),
                                      filetypes=(
                                          ("All files", "*.*"),
                                          ("Python files", "*.py"),
                                          ("JSON files", "*.json"),
                                          ("Batch files", "*.bat"),
                                          ("Shell files", "*.sh"),
                                      )
                                   )
        if self.current_script_path:
            try:
                code = self.ui.tk_text_output_code_text.get(1.0, END).replace('\r\n', '\n')
                with open(self.current_script_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                    f.close()
                    self.ui.tk_text_system_log_text.insert(END, f'文件保存成功：{self.current_script_path}\n')
            except Exception as e:
                self.ui.tk_text_system_log_text.insert(END, f'文件保存失败：{e}\n')
        else:
            self.ui.tk_text_system_log_text.insert(END, '文件保存已取消\n')

    def run_code_text_script(self, _):
        ''' 运行脚本 '''
        if self.ui.tk_button_run_code_button['text'] == '运行脚本':

            if self.output_type not in ['appium', 'adb']:
                self.ui.tk_text_system_log_text.insert(END, '仅支持appium、adb可以运行，source数据不支持运行\n')
                return
            self.ui.tk_button_run_code_button['text'] = '停止脚本'
            if not self.current_script_path:
                self.save_text_to_script(_)
            if self.current_script_path:
                Thread(target=self._monitor_start_stop_script_thread, daemon=True).start()
            else:
                self.ui.tk_button_run_code_button['text'] = '运行脚本'
                self.ui.tk_text_system_log_text.insert(END, '请先保存脚本\n')
        else:
            self._quit_process(self.run_script_process)
            self.ui.tk_text_system_log_text.insert(END, '运行脚本已停止\n')
            self.ui.tk_button_run_code_button['text'] = '运行脚本'

    def change_console_status(self, _):
        '''
        选择时将code_text控件宽度扩展到appium_text控件的宽度
        :param _:
        :return:
        '''
        # print(self.ui.check_status.get())

    def clear_system_log(self, _):
        ''' 清除系统日志 '''
        self.ui.tk_text_system_log_text.delete(1.0, END)

    def _monitor_appium_service_thread(self):
        try:
            command = 'appium server -p 4723 -a 127.0.0.1 -pa /wd/hub'
            command = self._system_console_command_format(command) if self.ui.check_status.get() else command
            self.appium_service_process = subprocess.Popen(command,
                                                           shell=True,
                                                           stdout=subprocess.PIPE,
                                                           stderr=subprocess.PIPE)
            _timeout = 10
            while not self._monitor_appium_service_status() and _timeout >= 0:
                sleep(0.5)
                _timeout -= 1
            if self.ui.check_status.get():
                # 勾选了console
                if self._monitor_appium_service_status():
                    self.ui.tk_text_system_log_text.insert(END, 'Appium服务已启动\n')
                    self.ui.tk_button_appium_status_button['text'] = '关闭Appium服务'
                else:
                    self.ui.tk_text_system_log_text.insert(END, 'Appium服务启动失败\n')
                    self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
                while self._monitor_appium_service_status(): sleep(0.5)
                self.ui.tk_text_system_log_text.insert(END, 'Appium服务已关闭\n')
                self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
                self.appium_service_process.terminate()
                self.appium_service_process.wait()
            else:
                # 未勾选console
                if self._monitor_appium_service_status():
                    self.ui.tk_text_system_log_text.insert(END, 'Appium服务已启动\n')
                    self.ui.tk_button_appium_status_button['text'] = '关闭Appium服务'
                    while self.appium_service_process.poll() is None:
                        try:
                            line = self.appium_service_process.stdout.readline()
                            if line:
                                line = line.decode('GB2312').strip()
                                self.ui.tk_text_appium_log_text.insert(END, line + '\n')
                        except Exception as e:
                            self.ui.tk_text_system_log_text.insert(END, f'Appium服务异常，{e}\n')
                            self._quit_process(self.appium_service_process)
                            self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
                            break
                    self.ui.tk_text_system_log_text.insert(END, 'Appium服务已关闭\n')
                    self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
                else:
                    self.ui.tk_text_system_log_text.insert(END, 'Appium服务启动失败\n')
                    self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
        except subprocess.CalledProcessError as e:
            self.ui.tk_button_appium_status_button['text'] = '启动Appium服务'
            try:
                self._quit_process(self.appium_service_process)
            except:
                pass
            self.ui.tk_text_system_log_text.insert(END, f'Appium服务启动失败，{e}\n')

    def _monitor_start_stop_script_thread(self):
        command = self._system_console_command_format(f'{PYTHON} {self.current_script_path}') \
            if self.output_type == 'appium' else self._system_console_command_format(self.current_script_path)
        try:
            self.ui.tk_text_system_log_text.insert(END, '准备运行...\n')
            self.run_script_process = subprocess.Popen(command, shell=True,
                                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while self.run_script_process.poll() == None:
                pass
            self.ui.tk_button_run_code_button['text'] = '运行脚本'
        except Exception as e:
            self.ui.tk_text_system_log_text.insert(END, f'运行脚本异常，{e}\n')
        self.ui.tk_button_run_code_button['text'] = '运行脚本'

    def convert_position(self, x, y, wx, wy):
        '''
        转换坐标
        :param x: 获取的x坐标
        :param y: 获取的y坐标
        :param wx: 当前页面的宽度
        :param wy: 当前页面的高度
        :return: new_x, new_y
        '''
        # 获取该设备x_max,y_max的值
        for line in os.popen('adb shell getevent -p').readlines():
            if '0035' in line and 'value' in line and 'min' in line and 'max' in line:
                ''' x '''
                ''' 0035  : value 0, min 0, max 8639, fuzz 0, flat 0, resolution 0 '''
                self.current_device_x_min, self.current_device_x_max = \
                    re.findall(r'0035.+min\s+(\d+),\s+max\s+(\d+),.+', line)[0]
            if '0036' in line and 'value' in line and 'min' in line and 'max' in line:
                ''' y '''
                ''' 0035  : value 0, min 0, max 8639, fuzz 0, flat 0, resolution 0 '''
                self.current_device_y_min, self.current_device_y_max = \
                    re.findall(r'0036.+min\s+(\d+),\s+max\s+(\d+),.+', line)[0]
        if int(self.current_device_x_max) == 0 or int(self.current_device_y_max) == 0:
            self.convert_position(x, y, wx, wy)
        else:
            new_x, new_y = int(x * wx / int(self.current_device_x_max)), int(y * wy / int(self.current_device_y_max))
            if new_x > wx or new_y > wy:
                self.convert_position(x, y, wx, wy)
            return new_x, new_y

    def _monitor_device_event_thread(self):
        ''' 监控设备发生的事件 '''
        if self.output_type not in ['source', 'appium', 'adb']:
            self.ui.tk_text_system_log_text.insert(END, '输出类型不支持\n')
            return
        global GETTIMER
        global tree
        device = self.current_device
        app = device.app_current()
        package_name = getattr(app, 'package')
        activity_name = getattr(app, 'activity')
        if self.output_type == 'source':
            header_code = f'''{{\
            \r\n\t'platformName': 'Android',\
            \r\n\t'platformVersion': '{device.getprop('ro.build.version.release').strip()}',\
            \r\n\t'deviceName': '{device.serial}',\
            \r\n\t'appPackage': '{package_name}',\
            \r\n\t'appActivity': '{activity_name}',\
            \r\n\t'actions': [\
            \r\n\t]\
            \r\n}}\n'''
            
        elif self.output_type == 'appium':
            header_code = f'''#! /usr/bin/env python
            \r\n#################################\
            \r\n#   Author: xiaobaiTser         #\
            \r\n#   Email : 807447312@qq.com    #\
            \r\n#################################
            \r\nfrom appium import webdriver\
            \r\nfrom appium.webdriver.common.mobileby import MobileBy as By\
            \r\nfrom time import sleep
            \r\ncaps = {{\
            \r\n    'automationName': 'UiAutomator2',\
            \r\n    'platformName': 'Android',\
            \r\n    'platformVersion': '{device.getprop('ro.build.version.release').strip()}',\
            \r\n    'deviceName': '{device.serial}',\
            \r\n    'appPackage': '{package_name}',\
            \r\n    'appActivity': '{activity_name}', # 不是启动页Activity，运行会报错！\
            \r\n    # 'noReset': True,\
            \r\n    # 'dontStopAppOnReset': True,\
            \r\n    # 'unicodeKeyboard': True,\
            \r\n    # 'resetKeyboard': True\
            \r\n}}
            \r\n###########################################################################################\
            \r\n# npm install -g appium                                            # 安装appium服务        #\
            \r\n# appium setup                                                     # 初始化appium服务      #\
            \r\n# appium server -p 4723 -a 127.0.0.1 -pa /wd/hub                   # 启动appium服务        #\
            \r\n# app = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)     # Appium 1.x default   #\
            \r\n# app = webdriver.Remote("http://127.0.0.1:4723/", caps)           # Appium 2.x default   #\
            \r\n###########################################################################################
            \r\napp = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
            \r\n# 以下为定位表达式
            \r\n'''
        else:
            if os.name == 'nt':
                header_code = f'''rem #################################\
                \r\nrem #   Author: xiaobaiTser         #\
                \r\nrem #   Email : 807447312@qq.com    #\
                \r\nrem #################################
                \r\nrem 关闭APP
                \r\nadb -s {device.serial} shell am force-stop {package_name}
                \r\nrem 启动APP
                \r\nadb -s {device.serial} shell am start {package_name}/{activity_name}
                \r\nrem 以下为操作指令（模拟点击与滑动）
                \r\n'''
            else:
                header_code = f'''#################################\
                \r\n#   Author: xiaobaiTser         #\
                \r\n#   Email : 807447312@qq.com    #\
                \r\n#################################
                \r\n# 启动APP
                \r\nadb -s {device.serial} shell am start -W {package_name}/{activity_name}
                \r\n# 以下为操作指令（模拟点击与滑动）
                \r\n'''
        self.ui.tk_text_output_code_text.delete(0.0, END)
        self.ui.tk_text_output_code_text.insert(INSERT, header_code)
        down_time = time()

        device_name = device.serial
        # 启动getevent命令，发布之前可以切换到子进程中
        event_command = f"adb -s {device_name} shell getevent -l"
        event_process = subprocess.Popen(event_command, stdout=subprocess.PIPE, shell=True)

        t = Thread(target=self._monitor_timer_threader, daemon=True)
        t.start()

        action = {
            'STATUS': [None, None],
            'DOWN_POSITION_X': -1,
            'DOWN_POSITION_Y': -1,
            'HOLD_TIME': 0,
            'UP_POSITION_X': -1,
            'UP_POSITION_Y': -1
        }
        # 解析事件流
        while device_name == device.serial:
            try:
                # 读取一行事件
                _line = event_process.stdout.readline()
                line = _line.decode(detect(_line)['encoding']).strip()
            except Exception as e:
                continue
            if line == '':
                continue

            # 如果是点击事件
            if "BTN_TOUCH" in line and "DOWN" in line:
                down_time = time()
                action = {
                    'STATUS': ['DOWN', None],
                    'DOWN_POSITION_X': -1,
                    'DOWN_POSITION_Y': -1,
                    'HOLD_TIME': 0,
                    'UP_POSITION_X': -1,
                    'UP_POSITION_Y': -1
                }
                # 生成 XML 文件
                device.shell(['uiautomator', 'dump'])
                # device.dump_hierarchy()
            # 获取x坐标
            if 'POSITION_X' in line and action['STATUS'][0] == 'DOWN':
                parts = line.split()
                if action['DOWN_POSITION_X'] == -1:
                    action['DOWN_POSITION_X'] = int(parts[3], 16)
                else:
                    action['UP_POSITION_X'] = int(parts[3], 16)

            if 'POSITION_Y' in line and action['STATUS'][0] == 'DOWN':
                parts = line.split()
                if action['DOWN_POSITION_Y'] == -1:
                    action['DOWN_POSITION_Y'] = int(parts[3], 16)
                else:
                    action['UP_POSITION_Y'] = int(parts[3], 16)

            # 如果是点击事件
            if "BTN_TOUCH" in line and "UP" in line:
                if action['DOWN_POSITION_X'] == -1 and action['DOWN_POSITION_Y'] == -1:
                    continue
                if action['UP_POSITION_X'] == -1 and action['UP_POSITION_Y'] == -1:
                    action['UP_POSITION_X'] = action['DOWN_POSITION_X']
                    action['UP_POSITION_Y'] = action['DOWN_POSITION_Y']
                action['STATUS'][1] = 'UP'
                action['HOLD_TIME'] = round(time() - down_time, 1)
                os.popen(f"adb -s {device.serial} pull /sdcard/window_dump.xml {UI_DUMP_FILE}")
                self.ui.tk_text_system_log_text.insert(END, f'action ==> {action}\n')
                while not os.path.exists(UI_DUMP_FILE) or os.path.getsize(UI_DUMP_FILE) == 0:
                    try:
                        if os.path.exists(UI_DUMP_FILE):  os.remove(UI_DUMP_FILE)
                    except FileNotFoundError as e:
                        pass
                    except PermissionError as e:
                        # 将 XML 文件保存到本地
                        os.popen(f"adb -s {device.serial} pull /sdcard/window_dump.xml {UI_DUMP_FILE}")
                        continue
                    finally:
                        # 将 XML 文件保存到本地
                        os.popen(f"adb -s {device.serial} pull /sdcard/window_dump.xml {UI_DUMP_FILE}")
                        # device.sync.pull('/sdcard/window_dump.xml', UI_DUMP_FILE)
                try:
                    # 解析 XML 文档
                    tree = etree.parse(UI_DUMP_FILE)
                except Exception as e:
                    continue
                elements = tree.xpath('//node')
                bounds = [[int(num) for num in re.findall(r'\d+', s)] for s in tree.xpath('//node/@bounds')]
                # 防止点击页面以外的坐标，限制x与y的最大值与最小值
                x_page_max = bounds[0][2]
                y_page_max = bounds[0][3]
                dx, dy = self.convert_position(action['DOWN_POSITION_X'], action['DOWN_POSITION_Y'], x_page_max, y_page_max)
                ux, uy = self.convert_position(action['UP_POSITION_X'], action['UP_POSITION_Y'], x_page_max, y_page_max)
                up_index = self.find_smallest_bounds_index((ux, uy), bounds)  # 查看是否再一个元素内，如果再就是点击
                down_index = self.find_smallest_bounds_index((dx, dy), bounds)
                if action['STATUS'] == ['DOWN', 'UP']:
                    GETTIMER = False
                    t.join()
                    del t
                    if up_index == down_index and abs(ux - dx) ** 2 < 1000 and abs(uy - dy) ** 2 < 1000:
                        if self.output_type == 'source':
                            sj = f"""\r\n\t\t{{\
                                \r\n\t\t\t'action': 'click',\
                                \r\n\t\t\t'xpath': '{self.generate_xpath_with_attributes(elements[up_index])}',\
                                \r\n\t\t\t'bounds': {[dx, dy, ux, uy]},\
                                \r\n\t\t\t'hold_time': {action['HOLD_TIME']}\
                                \r\n\t\t}},\
                                \r\n\t]\
                                \r\n}}"""
                            # 需要删除code_text的最后两行内容
                            self.ui.tk_text_output_code_text.delete('end - 3 lines', 'end')
                        elif self.output_type == 'appium':
                            sj = f'app.find_element(By.XPATH, value=\'{self.generate_xpath_with_attributes(elements[up_index])}\').click()'
                        else:
                            sj = 'adb shell input tap {} {} '.format(dx, dy)
                    else:
                        if self.output_type == 'source':
                            sj = f"""\r\n\t\t{{\
                                \r\n\t\t\t'action': 'swipe',\
                                \r\n\t\t\t'xpath': None,\
                                \r\n\t\t\t'bounds': {[dx, dy, ux, uy]},\
                                \r\n\t\t\t'hold_time':  {action['HOLD_TIME']}\
                                \r\n\t\t}},\
                                \r\n\t]\
                                \r\n}}"""
                            self.ui.tk_text_output_code_text.delete('end - 3 lines', 'end')
                        elif self.output_type == 'appium':
                            sj = f'app.swipe({dx}, {dy}, {ux}, {uy}, {int(action["HOLD_TIME"] * 1000)})'
                        else:
                            sj = 'adb shell input swipe {} {} {} {} {}'.format(dx, dy, ux, uy, int(action["HOLD_TIME"] * 1000))
                    action['STATUS'] = [None, None]
                    self.ui.tk_text_output_code_text.insert('end', sj + '\n')
                    t = Thread(target=self._monitor_timer_threader, daemon=True)
                    t.start()
        self._quit_process(event_process)

    def _monitor_device_screen_thread(self):
        while self.current_device is not None:
            try:
                screen = self.current_device.screenshot()
                screen = screen.resize((self.ui.tk_canvas_phone_ui.winfo_width(),
                                        self.ui.tk_canvas_phone_ui.winfo_height()),
                                        Image.LANCZOS)

                # 将 PIL 图像对象转换为 tkinter PhotoImage 对象
                current_device_ui = ImageTk.PhotoImage(screen)
                self.ui.tk_canvas_phone_ui.create_image(0, 0, image=current_device_ui, anchor='nw')
                sleep(0.5)
            except Exception or IOError:
                continue

    def _monitor_device_package_activity_thread(self):
        device_name = self.current_device_name
        device = self.current_device
        app = device.app_current()
        package_name = getattr(app, 'package')
        activity_name = getattr(app, 'activity')
        while True:
            try:
                if [package_name, activity_name] != [device.app_current().package, device.app_current().activity]:
                    app = device.app_current()
                    package_name = getattr(app, 'package')
                    activity_name = getattr(app, 'activity')
                    self.ui.tk_text_system_log_text.insert(END, f'当前设备:{device_name}  包名：{package_name}  activity：{activity_name}\n')
            except Exception or ConnectionResetError:
                pass
            sleep(1)

    def _monitor_logcat_threader(self):
        ''' 监控设备的logcat信息 '''
        command_old = f'adb -s {self.current_device.serial} logcat -v time'
        command = self._system_console_command_format(command_old)
        logcat_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 等待子进程结束
        while self.current_device is not None:
            sleep(1)
        self._quit_process(logcat_process)

    def _monitor_connect_device_list_thread(self):
        ''' 监控连接的设备名称并动态添加到下拉框中 '''
        device_list = []
        while True:
            new_device_list = [i.serial for i in adb.device_list()]
            self.ui.tk_select_box_connect_list['values'] = new_device_list
            # 判断new_device_list和device_list新增和缺少的值，写入系统日志中
            for device_name in new_device_list:
                if device_name not in device_list:
                    self.ui.tk_text_system_log_text.insert(END, f'设备[{device_name}]已上线\n')
            for device_name in device_list:
                if device_name not in new_device_list:
                    self.ui.tk_text_system_log_text.insert(END, f'设备[{device_name}]已下线\n')
            device_list = new_device_list
            sleep(0.5)

def main():
    app = Win(Controller())
    try:
        app.mainloop()
    except KeyboardInterrupt as e:
        pass

if __name__ == '__main__':
    main()