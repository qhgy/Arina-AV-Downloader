@echo off
echo.
echo ========================================
echo Arina AV Downloader v1.0.3 Installation
echo Thanks to Arina for 10 years of companionship
echo ========================================
echo.

echo [1/3] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found!
    echo Please install Python 3.8+: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [+] Python environment check passed
python --version

echo.
echo [2/3] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [3/3] Installing dependencies...
echo This may take a few minutes, please wait...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [!] Installation failed, trying with China mirror...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
)

if %errorlevel% neq 0 (
    echo [!] Dependency installation failed!
    echo Please check network connection or run manually: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [+] Installation completed!
echo.
echo Usage:
echo 1. GUI version: python arina_gui.py
echo 2. CLI version: python arina_cli.py --help
echo.
echo For detailed instructions, see: USER_GUIDE.md
echo.

echo.
echo Installation complete! Press Enter to start GUI version...
pause >nul
echo Starting GUI version...
python arina_gui.py
