@echo off
echo.
echo ========================================
echo Arina AV Downloader Full Installation Test
echo Automated testing: Download - Extract - Install - Run
echo ========================================
echo.

REM Set test directory
set TEST_DIR=d:\test_arina_auto
set GITHUB_URL=https://github.com/qhgy/Arina-AV-Downloader/archive/refs/tags/v1.0.9.zip
set ZIP_FILE=Arina-AV-Downloader-v1.0.9.zip
set EXTRACT_DIR=Arina-AV-Downloader-1.0.9

echo [1/5] Preparing test environment...
if exist "%TEST_DIR%" (
    echo Cleaning existing test directory...
    rmdir /s /q "%TEST_DIR%"
)
mkdir "%TEST_DIR%"
cd /d "%TEST_DIR%"

echo [2/5] Downloading latest release...
echo Downloading from: %GITHUB_URL%
curl -L -o "%ZIP_FILE%" "%GITHUB_URL%"
if %errorlevel% neq 0 (
    echo [!] Download failed!
    pause
    exit /b 1
)
echo [+] Download completed: %ZIP_FILE%

echo [3/5] Extracting archive...
powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '.' -Force"
if %errorlevel% neq 0 (
    echo [!] Extraction failed!
    pause
    exit /b 1
)
echo [+] Extraction completed

echo [4/5] Checking extracted files...
cd "%EXTRACT_DIR%"
if not exist "0-Install-UV-Recommended.bat" (
    echo [!] Installation script not found!
    dir
    pause
    exit /b 1
)
echo [+] Installation scripts found

echo [5/5] Running automated installation...
echo.
echo ==========================================
echo Starting UV installation (automated)...
echo ==========================================
echo.

REM Create automated input for installation
echo y | "0-Install-UV-Recommended.bat"

echo.
echo ==========================================
echo Installation test completed!
echo ==========================================
echo.
echo Test directory: %TEST_DIR%\%EXTRACT_DIR%
echo.
echo Manual verification steps:
echo 1. Check if .venv directory was created
echo 2. Check if dependencies were installed
echo 3. Try running: uv run python arina_gui.py
echo.

pause
