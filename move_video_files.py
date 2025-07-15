import os
import shutil

# Define source directory
source_dir = "."
target_dir = "vd"

# List of files to move
files_to_move = [
    "gui_downloader.py",
    "simple_downloader.py", 
    "simple_fallback.py",
    "simple_test_gui.py",
    "speed_optimizer.py",
    "test_pornhub.py",
    "direct_test.py",
    "minimal_test.py",
    "env_check.py",
    "force_blue_gui.py",
    "debug_gui.py",
    "requirements.txt",
    "downloader_config.json",
    "pornhub_cookies.json",
    "urls.txt",
    "test_urls.txt",
    "使用说明-增强版.md",
    "使用说明.md",
    "微信图片_20250713213155_236.jpg"
]

# Directories to move
dirs_to_move = [
    "cookies",
    "downloads", 
    "logs"
]

# Batch files to move (those related to video downloading)
batch_files = [
    "debug_gui.bat",
    "launch_fixed_gui.bat",
    "launch_gui.bat",
    "run_debug_gui.bat",
    "run_direct_test.bat",
    "run_pornhub_test.bat",
    "run_simple_test.bat",
    "start_gui.bat",
    "start_production.bat",
    "start_simple.bat",
    "start_turbo.bat",
    "start_with_cookies.bat",
    "test_batch_gui.bat",
    "test_blue_theme.bat",
    "test_dependencies.bat",
    "test_downloader.bat",
    "test_enhanced.bat",
    "test_fix.bat",
    "test_fixed_gui.bat",
    "test_fixed_theme.bat",
    "test_force_blue.bat",
    "test_gui_display.bat",
    "test_ui_progress.bat",
    "test_universal.bat",
    "test_with_cookies.bat"
]

# PowerShell files to move
ps_files = [
    "test_universal.ps1",
    "test_windows.ps1"
]

print("Moving video download files to vd directory...")

# Move individual files
for file in files_to_move:
    if os.path.exists(file):
        try:
            shutil.move(file, os.path.join(target_dir, file))
            print(f"Moved {file}")
        except Exception as e:
            print(f"Error moving {file}: {e}")

# Move batch files
for file in batch_files:
    if os.path.exists(file):
        try:
            shutil.move(file, os.path.join(target_dir, file))
            print(f"Moved {file}")
        except Exception as e:
            print(f"Error moving {file}: {e}")

# Move PowerShell files
for file in ps_files:
    if os.path.exists(file):
        try:
            shutil.move(file, os.path.join(target_dir, file))
            print(f"Moved {file}")
        except Exception as e:
            print(f"Error moving {file}: {e}")

# Move directories
for dir_name in dirs_to_move:
    if os.path.exists(dir_name):
        try:
            shutil.move(dir_name, os.path.join(target_dir, dir_name))
            print(f"Moved {dir_name} directory")
        except Exception as e:
            print(f"Error moving {dir_name}: {e}")

print("File moving completed!")