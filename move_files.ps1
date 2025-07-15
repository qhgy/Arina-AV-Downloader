# Move video download files to vd directory
Write-Host "Moving video download files to vd directory..."

# Python files
$pythonFiles = @(
    "enhanced_downloader.py",
    "multi_platform_downloader.py", 
    "universal_downloader.py",
    "youtube_downloader.py",
    "gui_downloader.py",
    "simple_downloader.py",
    "simple_fallback.py",
    "simple_test_gui.py",
    "speed_optimizer.py",
    "cookie_manager.py",
    "test_pornhub.py",
    "direct_test.py",
    "minimal_test.py",
    "env_check.py",
    "force_blue_gui.py",
    "debug_gui.py"
)

# Config and data files
$configFiles = @(
    "requirements.txt",
    "downloader_config.json",
    "pornhub_cookies.json",
    "urls.txt",
    "test_urls.txt"
)

# Directories
$directories = @(
    "cookies",
    "downloads",
    "logs"
)

# Move Python files
foreach ($file in $pythonFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "vd\" -Force
        Write-Host "Moved $file"
    }
}

# Move config files
foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "vd\" -Force
        Write-Host "Moved $file"
    }
}

# Move directories
foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Move-Item -Path $dir -Destination "vd\" -Force
        Write-Host "Moved $dir directory"
    }
}

# Move batch files
Get-ChildItem -Path "." -Filter "*.bat" | Where-Object { $_.Name -like "*gui*" -or $_.Name -like "*test*" -or $_.Name -like "*start*" -or $_.Name -like "*run*" -or $_.Name -like "*debug*" } | ForEach-Object {
    Move-Item -Path $_.FullName -Destination "vd\" -Force
    Write-Host "Moved $($_.Name)"
}

# Move PowerShell scripts related to video downloading
Get-ChildItem -Path "." -Filter "*.ps1" | Where-Object { $_.Name -like "*test*" -or $_.Name -like "*universal*" } | ForEach-Object {
    Move-Item -Path $_.FullName -Destination "vd\" -Force
    Write-Host "Moved $($_.Name)"
}

# Move markdown files related to video downloading
$mdFiles = @(
    "使用说明-增强版.md",
    "使用说明.md"
)

foreach ($file in $mdFiles) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination "vd\" -Force
        Write-Host "Moved $file"
    }
}

# Move image files if they're screenshots
if (Test-Path "微信图片_20250713213155_236.jpg") {
    Move-Item -Path "微信图片_20250713213155_236.jpg" -Destination "vd\" -Force
    Write-Host "Moved 微信图片_20250713213155_236.jpg"
}

Write-Host "All video download files moved to vd directory successfully!"