@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🌸 Arina AV Downloader UV虚拟环境安装
echo Thanks to Arina for 10 years of companionship 💕
echo ========================================
echo.

echo 📋 检查UV是否已安装...
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到UV！正在安装UV...
    echo 请稍等，这可能需要几分钟...
    
    REM 使用PowerShell安装UV
    powershell -Command "& {Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression}"
    
    if %errorlevel% neq 0 (
        echo ❌ UV安装失败！
        echo 请手动安装UV：https://docs.astral.sh/uv/getting-started/installation/
        pause
        exit /b 1
    )
    
    echo ✅ UV安装成功！
    echo 请重新运行此脚本或重启命令提示符
    pause
    exit /b 0
)

echo ✅ UV环境检查通过
uv --version

echo.
echo 🔧 创建虚拟环境...
uv venv

echo.
echo 📦 安装项目依赖...
echo 这可能需要几分钟时间，请耐心等待...

REM 激活虚拟环境并安装依赖
uv pip install -e .

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败！
    echo 尝试单独安装核心依赖...
    uv pip install yt-dlp PySide6 requests colorama tqdm jsonschema
)

if %errorlevel% neq 0 (
    echo ❌ 安装失败！请检查网络连接
    pause
    exit /b 1
)

echo.
echo ✅ 安装完成！
echo.
echo 🚀 使用方法：
echo.
echo 1. 激活虚拟环境：
echo    .venv\Scripts\activate
echo.
echo 2. 启动程序：
echo    python arina_gui.py    (GUI版本)
echo    python arina_cli.py    (CLI版本)
echo.
echo 3. 或者直接使用UV运行：
echo    uv run python arina_gui.py
echo    uv run python arina_cli.py
echo.

set /p choice="是否现在启动GUI版本？(y/n): "
if /i "%choice%"=="y" (
    echo 启动GUI版本...
    uv run python arina_gui.py
) else (
    echo 安装完成！
    echo 记住：使用前需要先激活虚拟环境或使用 'uv run' 命令
)

pause
