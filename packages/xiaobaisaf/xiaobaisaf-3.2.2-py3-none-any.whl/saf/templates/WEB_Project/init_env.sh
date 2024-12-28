#!/usr/bin/env bash

# 设置窗口标题（适用于 macOS）
echo -e "\033]0;正在运行...\007"

# 检查虚拟环境是否已存在
if [ -d "venv" ]; then
    # 如果虚拟环境存在且未激活，激活虚拟环境
    if [ -z "${VIRTUAL_ENV}" ]; then
        echo "正在激活虚拟环境..."
        source venv/bin/activate
    else
        echo "虚拟环境已激活。"
    fi
else
    # 如果虚拟环境不存在，则创建并激活
    echo "正在创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
fi

# 安装依赖并检查是否成功
echo "正在安装依赖..."
pip install -r requirements.txt --upgrade
if [ $? -ne 0 ]; then
    echo "安装依赖失败。"
    deactivate
    exit 1
fi

# 执行 Python 脚本并检查是否成功
echo "正在运行 convert_ui.py..."
python convert_ui.py
if [ $? -ne 0 ]; then
    echo "运行 convert_ui.py 失败。"
    deactivate
    exit 1
fi

# 脚本完成
echo "所有任务已成功完成。"
deactivate

