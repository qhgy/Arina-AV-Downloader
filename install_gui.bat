@echo off
echo Installing PyQt6 for modern GUI interface...
echo.

pip install PyQt6
if %errorlevel% neq 0 (
    echo PyQt6 installation failed, trying PySide6...
    pip install PySide6
    if %errorlevel% neq 0 (
        echo Both PyQt6 and PySide6 installation failed.
        echo Please install manually: pip install PyQt6
        pause
        exit /b 1
    )
)

echo.
echo ✅ GUI framework installed successfully!
echo.
echo You can now run the modern GUI interface:
echo   python gui_downloader.py
echo.

pause