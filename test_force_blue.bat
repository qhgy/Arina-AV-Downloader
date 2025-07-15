@echo off
echo ===== Force Sky Blue Background GUI =====
echo.
echo This version forces sky blue background on ALL widgets
echo to eliminate any black/dark areas completely.
echo.
echo If you still see black areas after this, 
echo it might be a PyQt/system-specific rendering issue.
echo.

cd /d D:\000cc
python force_blue_gui.py

echo.
pause