@echo off
:: SETLOCAL

REM 设置标题
title Running...

REM 检查虚拟环境目录是否存在，不存在则创建
IF NOT EXIST "venv" (
    echo 创建虚拟环境中...
    python -m venv venv
) ELSE (
    echo 虚拟环境已经存在。
)

REM 激活虚拟环境
IF NOT DEFINED _OLD_VIRTUAL_PROMPT (
    call venv\Scripts\activate.bat
)

REM 安装依赖
echo 安装依赖中...
pip install -r requirements.txt --upgrade
IF %ERRORLEVEL% NEQ 0 (
    echo 安装依赖失败.
    ENDLOCAL
    EXIT /B 1
)



REM 环境准备完毕，执行其他任务
echo 环境准备完毕，执行其他任务。
:: ENDLOCAL
