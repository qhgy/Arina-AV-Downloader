@echo off
echo Moving video download related files to vd directory...

REM Move Python files
move "debug_gui.py" "vd\debug_gui.py"
move "simple_fallback.py" "vd\simple_fallback.py"
move "minimal_test.py" "vd\minimal_test.py"
move "direct_test.py" "vd\direct_test.py"
move "simple_test_gui.py" "vd\simple_test_gui.py"
move "test_pornhub.py" "vd\test_pornhub.py"
move "speed_optimizer.py" "vd\speed_optimizer.py"
move "move_video_files.py" "vd\move_video_files.py"
move "env_check.py" "vd\env_check.py"

REM Move configuration files
move "downloader_config.json" "vd\downloader_config.json"
move "requirements.txt" "vd\requirements.txt"
move "test_urls.txt" "vd\test_urls.txt"
move "urls.txt" "vd\urls.txt"

REM Move batch files
move "debug_gui.bat" "vd\debug_gui.bat"
move "launch_fixed_gui.bat" "vd\launch_fixed_gui.bat"
move "launch_gui.bat" "vd\launch_gui.bat"
move "run_debug_gui.bat" "vd\run_debug_gui.bat"
move "run_direct_test.bat" "vd\run_direct_test.bat"
move "run_pornhub_test.bat" "vd\run_pornhub_test.bat"
move "run_simple_test.bat" "vd\run_simple_test.bat"
move "start_gui.bat" "vd\start_gui.bat"
move "start_production.bat" "vd\start_production.bat"
move "start_simple.bat" "vd\start_simple.bat"
move "start_turbo.bat" "vd\start_turbo.bat"
move "start_with_cookies.bat" "vd\start_with_cookies.bat"
move "test_batch_gui.bat" "vd\test_batch_gui.bat"
move "test_blue_theme.bat" "vd\test_blue_theme.bat"
move "test_dependencies.bat" "vd\test_dependencies.bat"
move "test_downloader.bat" "vd\test_downloader.bat"
move "test_enhanced.bat" "vd\test_enhanced.bat"
move "test_fix.bat" "vd\test_fix.bat"
move "test_fixed_gui.bat" "vd\test_fixed_gui.bat"
move "test_fixed_theme.bat" "vd\test_fixed_theme.bat"
move "test_force_blue.bat" "vd\test_force_blue.bat"
move "test_gui_display.bat" "vd\test_gui_display.bat"
move "test_ui_progress.bat" "vd\test_ui_progress.bat"
move "test_universal.bat" "vd\test_universal.bat"
move "test_with_cookies.bat" "vd\test_with_cookies.bat"
move "install_gui.bat" "vd\install_gui.bat"

REM Move PowerShell files
move "move_files.ps1" "vd\move_files.ps1"
move "test_universal.ps1" "vd\test_universal.ps1"
move "test_windows.ps1" "vd\test_windows.ps1"
move "install_and_test.ps1" "vd\install_and_test.ps1"

REM Move cookies and related files
move "cookies" "vd\cookies"
move "pornhub_cookies.json" "vd\pornhub_cookies.json"

REM Move downloads directory
move "downloads" "vd\downloads"

REM Move documentation files
move "使用说明-增强版.md" "vd\使用说明-增强版.md"
move "使用说明.md" "vd\使用说明.md"

echo Done moving files!
pause