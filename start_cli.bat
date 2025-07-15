@echo off
:: Arina AV Downloader - 简化启动脚本
:: 调用PowerShell处理复杂逻辑，避免中文乱码

title Arina AV Downloader

:: 检查PowerShell是否可用
powershell -Command "exit 0" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PowerShell not available
    echo Please install PowerShell or use launcher.py
    pause
    exit /b 1
)

:: 调用PowerShell脚本处理主要逻辑
powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"

:: 传递PowerShell的退出码
exit /b %errorlevel%