@echo off

REM 设置标题
title Running main.py...
python main.py
IF %ERRORLEVEL% NEQ 0 (
    echo 运行main.py失败.
    ENDLOCAL
    EXIT /B 1
)