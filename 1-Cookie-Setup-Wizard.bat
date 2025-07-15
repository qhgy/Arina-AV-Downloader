@echo off
echo.
echo ========================================
echo Arina Cookie Setup Wizard
echo For better download experience
echo ========================================
echo.

echo [INFO] This wizard helps you set up cookies for:
echo    - Downloading private/premium content
echo    - Accessing your account's saved videos
echo    - Better download success rates
echo.

echo [REQUIREMENTS] What you'll need:
echo    - EditThisCookie browser extension
echo    - Login to your video website account
echo    - 2-3 minutes of your time
echo.

set /p choice="Ready to start cookie setup? (y/n): "
if /i "%choice%" neq "y" (
    echo Setup cancelled. You can run this anytime!
    pause
    exit /b 0
)

echo.
echo [STARTING] Cookie Setup Wizard...
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    .venv\Scripts\python.exe cookie_setup_wizard.py
) else (
    echo Using system Python...
    python cookie_setup_wizard.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Cookie setup failed!
    echo Please make sure Python is installed and try again.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Cookie setup completed!
pause
