# PowerShell Test Script for Universal Video Downloader

Write-Host "Universal Multi-Platform Video Downloader v2.0 - Test Script" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Cyan

# Check Python
Write-Host "`nChecking Python environment..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "SUCCESS: Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found, please install Python 3.7+" -ForegroundColor Red
    exit 1
}

# Check package manager
Write-Host "`nChecking package manager..." -ForegroundColor Yellow
$hasUv = $false
try {
    $uvVersion = uv --version 2>&1
    Write-Host "SUCCESS: Detected uv: $uvVersion" -ForegroundColor Green
    $hasUv = $true
} catch {
    Write-Host "INFO: uv not detected, will use pip for dependencies" -ForegroundColor Yellow
}

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
if ($hasUv) {
    Write-Host "Using uv to install yt-dlp..." -ForegroundColor Cyan
    uv add yt-dlp
} else {
    Write-Host "Using pip to install yt-dlp..." -ForegroundColor Cyan
    python -m pip install yt-dlp
}

# Test core module
Write-Host "`nTesting core module..." -ForegroundColor Yellow
try {
    python -c "from universal_downloader import PlatformDetector; print('Platform detection test passed')"
    Write-Host "SUCCESS: Core module test passed" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Core module test failed" -ForegroundColor Red
    exit 1
}

# Test CLI
Write-Host "`nTesting command line interface..." -ForegroundColor Yellow
Write-Host "Showing supported platforms:" -ForegroundColor Cyan
python universal_cli.py --platforms

Write-Host "`nShowing configuration:" -ForegroundColor Cyan
python universal_cli.py --config

Write-Host "`nTesting help display:" -ForegroundColor Cyan
python universal_cli.py --help

Write-Host "`nSUCCESS: All tests completed!" -ForegroundColor Green
Write-Host "`nUsage examples:" -ForegroundColor Yellow
Write-Host "  Basic download: python universal_cli.py 'https://youtube.com/watch?v=...'" -ForegroundColor White
Write-Host "  Audio download: python universal_cli.py -a 'URL'" -ForegroundColor White
Write-Host "  View info: python universal_cli.py -i 'URL'" -ForegroundColor White
Write-Host "  Batch download: python universal_cli.py -b urls.txt" -ForegroundColor White

Read-Host "`nPress any key to continue..."