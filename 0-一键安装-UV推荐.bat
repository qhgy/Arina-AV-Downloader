@echo off
echo.
echo ========================================
echo Arina AV Downloader v1.0.3 UV Installation
echo Thanks to Arina for 10 years of companionship
echo ========================================
echo.

echo [1/4] Checking UV installation...
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] UV not found! Installing UV...
    echo Please wait, this may take a few minutes...

    REM Install UV using PowerShell
    powershell -Command "& {Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression}"

    if %errorlevel% neq 0 (
        echo [!] UV installation failed!
        echo Please install UV manually: https://docs.astral.sh/uv/getting-started/installation/
        pause
        exit /b 1
    )

    echo [+] UV installation successful!
    echo Please restart this script or command prompt
    pause
    exit /b 0
)

echo [+] UV environment check passed
uv --version

echo.
echo [2/4] Creating virtual environment...
uv venv

echo.
echo [3/4] Installing project dependencies...
echo This may take a few minutes, please wait...

REM Install dependencies from requirements.txt
uv pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [!] Dependency installation failed!
    echo Trying to install core dependencies separately...
    uv pip install yt-dlp PySide6 requests colorama tqdm jsonschema
)

if %errorlevel% neq 0 (
    echo [!] Installation failed! Please check network connection
    pause
    exit /b 1
)

echo.
echo [4/4] Installation completed!
echo.
echo Usage:
echo.
echo 1. Activate virtual environment:
echo    .venv\Scripts\activate
echo.
echo 2. Start program:
echo    python arina_gui.py    (GUI version)
echo    python arina_cli.py    (CLI version)
echo.
echo 3. Or use UV directly:
echo    uv run python arina_gui.py
echo    uv run python arina_cli.py
echo.

echo.
echo Installation complete! Press Enter to start GUI version...
pause >nul
echo Starting GUI version...
uv run python arina_gui.py
