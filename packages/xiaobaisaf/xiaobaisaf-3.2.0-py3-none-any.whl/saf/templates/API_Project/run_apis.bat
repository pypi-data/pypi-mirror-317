@echo off

REM 设置标题
title Running convert_ui.py...
python convert_ui.py
IF %ERRORLEVEL% NEQ 0 (
    echo 运行convert_ui.py失败.
    ENDLOCAL
    EXIT /B 1
)