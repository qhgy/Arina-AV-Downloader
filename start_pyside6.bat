@echo off
:: Universal Video Downloader - PySide6 GUI启动脚本
:: 使用全新的Apple风格界面

title Universal Video Downloader - PySide6 GUI

:: 检查PowerShell是否可用
powershell -Command "exit 0" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PowerShell not available
    echo Please install PowerShell or run python pyside6_gui.py directly
    pause
    exit /b 1
)

:: 调用PowerShell脚本处理主要逻辑
powershell -ExecutionPolicy Bypass -File "%~dp0start_pyside6.ps1"

:: 传递PowerShell的退出码
exit /b %errorlevel%
