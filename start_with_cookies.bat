@echo off
echo.
echo ████████████████████████████████████████████████████████████
echo ███                                                      ███
echo ███     Universal Video Downloader v2.0 + Cookies       ███
echo ███              Simple • Fast • Clean                   ███
echo ███                                                      ███
echo ████████████████████████████████████████████████████████████
echo.
echo Starting downloader with cookie support...
echo.

cd /d D:\000cc

echo Testing cookie manager...
python cookie_manager.py

echo.
echo Launching simple downloader...
python simple_downloader.py

echo.
echo Thanks for using Universal Video Downloader!
pause