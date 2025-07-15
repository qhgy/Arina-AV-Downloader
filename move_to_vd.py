#!/usr/bin/env python3
"""
Move video download related files to vd directory
"""

import shutil
import os
from pathlib import Path

def move_files():
    """Move all video download related files to vd directory"""
    source_dir = Path(".")
    target_dir = Path("vd")
    
    # Ensure target directory exists
    target_dir.mkdir(exist_ok=True)
    
    # Files to move
    files_to_move = [
        # Python files
        "debug_gui.py",
        "simple_fallback.py", 
        "minimal_test.py",
        "direct_test.py",
        "simple_test_gui.py",
        "test_pornhub.py",
        "speed_optimizer.py",
        "move_video_files.py",
        "env_check.py",
        
        # Batch files  
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
        "test_with_cookies.bat",
        "install_gui.bat",
        
        # PowerShell files
        "move_files.ps1",
        "test_universal.ps1", 
        "test_windows.ps1",
        "install_and_test.ps1",
        
        # JSON files
        "pornhub_cookies.json",
        
        # Documentation
        "使用说明-增强版.md",
    ]
    
    # Directories to move
    dirs_to_move = [
        "cookies",
        "downloads",
    ]
    
    moved_count = 0
    
    print("Moving files...")
    
    # Move individual files
    for file_name in files_to_move:
        source_path = source_dir / file_name
        target_path = target_dir / file_name
        
        if source_path.exists():
            try:
                if target_path.exists():
                    target_path.unlink()  # Remove existing file
                shutil.move(str(source_path), str(target_path))
                print(f"Moved: {file_name}")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {file_name}: {e}")
        else:
            print(f"File not found: {file_name}")
    
    # Move directories
    for dir_name in dirs_to_move:
        source_path = source_dir / dir_name
        target_path = target_dir / dir_name
        
        if source_path.exists() and source_path.is_dir():
            try:
                if target_path.exists():
                    shutil.rmtree(str(target_path))  # Remove existing directory
                shutil.move(str(source_path), str(target_path))
                print(f"Moved directory: {dir_name}")
                moved_count += 1
            except Exception as e:
                print(f"Error moving directory {dir_name}: {e}")
        else:
            print(f"Directory not found: {dir_name}")
    
    print(f"\nTotal files/directories moved: {moved_count}")
    print("Done!")

if __name__ == "__main__":
    move_files()