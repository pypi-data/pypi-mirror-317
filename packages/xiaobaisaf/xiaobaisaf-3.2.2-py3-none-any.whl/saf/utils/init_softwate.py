#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: xiaobaiTser
@Time  : 2023/12/24 1:01
@File  : init_softwate.py
"""

from urllib3 import PoolManager
from zipfile import ZipFile
import flet as ft
import os
import re
import platform

"""
1、检测adb及版本，若不存在则提示安装并提供下载链接或者按钮
"""


def main(page: ft.Page):
    page.title = "小白·测试软件工具包"
    page.icon = "favicon.ico"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 垂直居中
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平居中
    page.window_width = 300
    page.window_height = 600

    adb_col = ft.Column(
        width=300,
    )
    jdk_col = ft.Column(
        width=300,
    )
    jmeter_col = ft.Column(
        width=300,
    )
    env_col = ft.Column(
        width=300,
    )

    _check_info_message = ft.Text("", color="red")
    check_adb_message = ft.Text("", color="red")
    check_jdk_message = ft.Text("", color="red")
    check_jmeter_message = ft.Text("", color="red")

    _os_name = platform.system().lower()

    database = {
        "windows": {
            "adb-url": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
            "openjdk-url": "",
            "jmeter-url": "",
            "pathLimiter": "\\",
            "envLimiter": ";",
        },
        "linux": {
            "url": "https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
            "openjdk-url": "",
            "jmeter-url": "",
            "pathLimiter": "/",
            "envLimiter": ":",
        },
        "darwin": {
            "url": "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip",
            "openjdk-url": "",
            "jmeter-url": "",
            "pathLimiter": "/",
            "envLimiter": ":",
        },
    }

    def check_adb(e):
        """检测adb及版本,若不存在则提示安装并提供下载链接或者按钮"""
        version_info = (
            re.findall("[\d\.]+", os.popen("adb version").read())[0]
            if "version" in os.popen("adb version").read()
            else None
        )
        if version_info:
            check_adb_message.value = f"ADB版本:[{version_info}]"
            page.update()
        else:

            def slef_install_adb(e):
                page.launch_url(database[_os_name]["adb-url"])

            def auto_install_adb(e):
                """1、下载  2、解压  3、设置环境变量"""
                try:
                    check_adb_message.value = "正在下载ADB..."
                    page.update()
                    data = PoolManager().request("GET", database[_os_name]["adb-url"])
                    with open("platform-tools.zip", "wb") as f:
                        f.write(data.data)
                        f.close()

                    try:
                        check_adb_message.value = "正在解压【platform-tools.zip】..."
                        page.update()
                        # 解压
                        ZipFile("platform-tools.zip", "r").extractall()
                        os.remove("platform-tools.zip")
                    except:
                        check_adb_message.value = "解压失败，请手动解压【platform-tools.zip】"
                        page.update()
                    # 获取当前路径
                    current_path = (
                        os.getcwd()
                        + database[_os_name]["pathLimiter"]
                        + "platform-tools"
                        + database[_os_name]["pathLimiter"]
                    )

                    check_adb_message.value = "正在设置ADB的临时环境变量..."
                    page.update()
                    if permanent_env_box.value:
                        # 设置永久环境变量
                        os.environ["PATH"] = current_path
                    else:
                        # 设置临时环境变量
                        os.environ["PATH"] = (
                            os.environ["PATH"]
                            + database[_os_name]["envLimiter"]
                            + current_path
                        )
                    check_adb_message.value = "ADB已经安装，请重新检查ADB环境..."
                    # 重新加载页面，删除安装按钮和提示信息，只显示检查按钮
                    adb_col.controls = [check_adb_button, check_adb_message]
                    page.update()

                except Exception as e:
                    check_adb_message.value = "自动安装失败，请选择手动下载adb"

            _self_button = ft.ElevatedButton(
                text="仅下载ADB",
                on_click=slef_install_adb,
                icon=ft.icons.ADB,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                ),
            )
            _auto_button = ft.ElevatedButton(
                text="自动下载ADB并配置环境变量",
                on_click=auto_install_adb,
                icon=ft.icons.ADB,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                ),
            )

            check_adb_message.value = "未找到adb或者未添加到PATH环境中！"

            adb_col.controls = [_self_button, _auto_button, check_adb_message]
            page.add(
                env_col,
            )
            page.update()

    def check_jdk(e):
        ...

    def check_jmeter(e):
        ...

    # 选择临时环境变量和永久环境变量
    def temporary_env(e):
        """选择临时环境变量"""
        temporary_env_box.value = True
        permanent_env_box.value = False
        page.update()

    def permanent_env(e):
        """选择永久环境变量"""
        temporary_env_box.value = False
        permanent_env_box.value = True
        page.update()

    temporary_env_box = ft.Checkbox(label="临时环境变量", value=True, on_change=temporary_env)
    permanent_env_box = ft.Checkbox(
        label="永久环境变量", value=False, on_change=permanent_env
    )

    check_adb_button = ft.ElevatedButton(
        text="检查ADB环境",
        on_click=check_adb,
        icon=ft.icons.CHECK,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        ),
    )

    check_jdk_button = ft.ElevatedButton(
        text="检查JDK环境",
        on_click=check_jdk,
        icon=ft.icons.CHECK,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        ),
    )

    check_jmeter_button = ft.ElevatedButton(
        text="检查JMeter环境",
        on_click=check_jmeter,
        icon=ft.icons.CHECK,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
        ),
    )

    adb_col.controls = [check_adb_message, check_adb_button]
    jdk_col.controls = [check_jdk_message, check_jdk_button]
    jmeter_col.controls = [check_jmeter_message, check_jmeter_button]
    env_col.controls = [temporary_env_box, permanent_env_box]  # 需要安装软件时再展示

    page.add(
        _check_info_message,
        adb_col,
        jdk_col,
        jmeter_col,
    )

    # page.add(
    #     _check_info_message,
    #     check_adb_button,
    # )
    page.update()


ft.app(target=main)
