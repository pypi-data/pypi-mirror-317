@echo off

REM 设置标题
title Running run_apis.py...
python run_apis.py
IF %ERRORLEVEL% NEQ 0 (
    echo 运行run_apis.py失败.
    ENDLOCAL
    EXIT /B 1
)