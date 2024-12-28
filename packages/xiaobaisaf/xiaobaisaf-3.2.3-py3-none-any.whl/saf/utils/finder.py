#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2024/1/31 23:25
@File  : finder2.py
'''

import os
import platform
import sqlite3
import subprocess
import tkinter as tk
from tkinter import ttk
from threading import Thread

# 创建主窗口及组件
root = tk.Tk()
root.title("文件搜索器@xiaobaiTser")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

search_text = tk.StringVar()
search_text.set("请输入要搜索的关键字")

FILE_DB_NAME = os.path.expanduser('~') + '/.df.db'

# 创建数据库表结构
def init_database():
    ''' 初始化数据库表结构 '''
    conn = sqlite3.connect(FILE_DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  path TEXT UNIQUE NOT NULL)''')
    conn.commit()
    # 获取表中所有行数，使用最优方法获取行数
    c.execute("SELECT COUNT(*) FROM files")
    row_count = c.fetchone()[0]
    for num in range(0, row_count, 1000):
        c.execute("SELECT id, path FROM files LIMIT 1000 OFFSET ?", (num,))
        for _id, _path in c.fetchall():
            if not os.path.exists(_path):
                c.execute("DELETE FROM files WHERE id=?", (_id,))
        conn.commit()
    conn.close()

# 遍历磁盘并填充索引
def build_index():
    ''' 构建索引 '''
    global root
    conn = sqlite3.connect(FILE_DB_NAME, check_same_thread=False)
    c = conn.cursor()

    if platform.system() == 'Windows':
        # 获取Windows系统下的所有本地磁盘
        for drive_letter in ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:\\' % d)]:
            root_path = drive_letter + '\\'
            for dirpath, dirs, files in os.walk(root_path):
                root.title(f'文件搜索器@xiaobaiTser <正在扫描{dirpath}...>')
                for filename in files + dirs:
                    full_path = os.path.join(dirpath, filename)
                    c.execute("INSERT OR IGNORE INTO files (name, path) VALUES (?, ?)",
                              (filename, full_path))
                conn.commit()


    else:  # 类Unix系统或其他非Windows系统
        for _root, _dirs, _files in os.walk('/'):
            root.title(f'文件搜索器@xiaobaiTser <正在扫描{root}...>')
            for filename in _files + _dirs:
                full_path = os.path.join(_root, filename)
                c.execute("INSERT OR IGNORE INTO files (name, path) VALUES (?, ?)",
                          (filename, full_path))
            conn.commit()
    conn.close()
    root.title('文件搜索器@xiaobaiTser <扫描磁盘完毕>')

def search_input_focus(event):
    ''' 搜索输入框获取焦点 '''
    if search_text.get() == "请输入要搜索的关键字":
        search_text.set("")

# 实现查询与结果显示在表格控件中
def search_files(event):
    ''' 搜索文件 '''
    search_value = search_text.get().lower().strip()
    results_table.delete(*results_table.get_children())

    if not search_value:
        return
    conn = sqlite3.connect(FILE_DB_NAME, check_same_thread=False)
    c = conn.cursor()
    if '*' in search_value:
        search_value = search_value.replace('*', '%')
        query = f'SELECT id, name, path FROM files WHERE lower(name) LIKE \'{search_value}\''
    else:
        query = f'SELECT id, name, path FROM files WHERE lower(name) LIKE \'%{search_value}%\''
    c.execute(query)

    for row_id, name, path in c.fetchall():
        results_table.insert('', 'end', values=(row_id, name, path))

    conn.close()

def search_file_thread(event):
    ''' 搜索文件线程 '''
    Thread(target=search_files, args=(event,)).start()

# 定义复制完整路径到剪贴板的函数
def copy_path_to_clipboard():
    ''' 复制完整路径到剪贴板 '''
    item = results_table.focus()
    if item:
        row_values = results_table.item(item, 'values')
        if row_values:
            path = row_values[2]  # 获取第三列即路径
            root.clipboard_clear()
            root.clipboard_append(path)
            root.title('文件搜索器@xiaobaiTser <已复制路径>')

def open_path():
    ''' 打开路径 '''
    item = results_table.focus()
    if item:
        row_values = results_table.item(item, 'values')
        if row_values:
            path = os.path.dirname(row_values[2])  # 获取第三列即路径
            if platform.system() == 'Windows':
                subprocess.Popen(f'explorer "{path}"')
            else:
                subprocess.Popen(f'open "{path}"')

search_frame = ttk.Frame(root, height=50)
search_frame.pack(fill=tk.BOTH, padx=2, pady=10)
# 搜索框
search_input = ttk.Entry(search_frame, textvariable=search_text)
search_input.bind("<FocusIn>", search_input_focus)
search_input.bind("<Return>", search_file_thread)
search_input.pack(fill=tk.BOTH, expand=True)

# 结果表格
columns = ('ID', '文件/目录名', '路径')
results_table = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    results_table.heading(col, text=col)
results_table.pack(fill=tk.BOTH, expand=True)

# 右键菜单 - 复制路径
context_menu = tk.Menu(results_table, tearoff=0)
context_menu.add_command(label="复制路径", command=copy_path_to_clipboard)
context_menu.add_command(label="打开路径", command=open_path)
results_table.bind("<Button-3>", lambda e: context_menu.post(e.x_root, e.y_root))

def main():
    # 初始化数据库和索引
    Thread(target=init_database).start()
    Thread(target=build_index).start()
    root.mainloop()