@echo off
echo.
echo ========================================
echo Arina AV Downloader - Daily Use
echo Starting GUI Interface
echo ========================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo [INFO] Using UV virtual environment...
    echo [STARTING] Arina GUI...
    echo.
    .venv\Scripts\python.exe arina_gui.py
) else (
    echo [INFO] Virtual environment not found, using system Python...
    echo [STARTING] Arina GUI...
    echo.
    python arina_gui.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start GUI!
    echo Please make sure the installation completed successfully.
    echo Try running the installation script again.
    pause
    exit /b 1
)

echo.
echo [INFO] GUI closed normally.
pause
