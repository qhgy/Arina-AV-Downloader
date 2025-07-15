@echo off
echo Moving video download files to vd directory...

move enhanced_downloader.py vd\ 2>nul
move multi_platform_downloader.py vd\ 2>nul
move universal_downloader.py vd\ 2>nul
move youtube_downloader.py vd\ 2>nul
move gui_downloader.py vd\ 2>nul
move simple_downloader.py vd\ 2>nul
move simple_fallback.py vd\ 2>nul
move simple_test_gui.py vd\ 2>nul
move speed_optimizer.py vd\ 2>nul
move cookie_manager.py vd\ 2>nul
move test_pornhub.py vd\ 2>nul
move direct_test.py vd\ 2>nul
move minimal_test.py vd\ 2>nul
move env_check.py vd\ 2>nul
move force_blue_gui.py vd\ 2>nul
move debug_gui.py vd\ 2>nul
move requirements.txt vd\ 2>nul
move downloader_config.json vd\ 2>nul
move pornhub_cookies.json vd\ 2>nul
move urls.txt vd\ 2>nul
move test_urls.txt vd\ 2>nul

move cookies vd\ 2>nul
move downloads vd\ 2>nul
move logs vd\ 2>nul

move *.bat vd\ 2>nul
move *.ps1 vd\ 2>nul
move *.md vd\ 2>nul
move *.jpg vd\ 2>nul

echo Files moved to vd directory successfully!
pause