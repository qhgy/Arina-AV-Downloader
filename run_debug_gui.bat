@echo off
echo ===== Debug GUI Test =====
echo.
echo This will show exactly what happens during GUI download
echo with detailed logging and error messages.
echo.
echo Since CLI download worked, this will help identify
echo what's different in the GUI implementation.
echo.

cd /d D:\000cc

echo Launching Debug GUI...
echo.

python debug_gui.py

echo.
echo Debug session ended.
pause