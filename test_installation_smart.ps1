# Arina AV Downloader Smart Installation Test
# PowerShell version with better automation

param(
    [string]$TestDir = "d:\test_arina_smart",
    [string]$Version = "v1.0.9"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Arina AV Downloader Smart Installation Test" -ForegroundColor Cyan
Write-Host "Testing version: $Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$GitHubUrl = "https://github.com/qhgy/Arina-AV-Downloader/archive/refs/tags/$Version.zip"
$ZipFile = "Arina-AV-Downloader-$Version.zip"
$ExtractDir = "Arina-AV-Downloader-$($Version.Substring(1))"

try {
    # Step 1: Prepare environment
    Write-Host "[1/6] Preparing test environment..." -ForegroundColor Yellow
    if (Test-Path $TestDir) {
        Write-Host "Cleaning existing test directory..." -ForegroundColor Gray
        Remove-Item -Recurse -Force $TestDir
    }
    New-Item -ItemType Directory -Path $TestDir | Out-Null
    Set-Location $TestDir
    Write-Host "[+] Test environment ready: $TestDir" -ForegroundColor Green

    # Step 2: Download
    Write-Host "[2/6] Downloading release..." -ForegroundColor Yellow
    Write-Host "URL: $GitHubUrl" -ForegroundColor Gray
    Invoke-WebRequest -Uri $GitHubUrl -OutFile $ZipFile -UseBasicParsing
    Write-Host "[+] Download completed: $ZipFile" -ForegroundColor Green

    # Step 3: Extract
    Write-Host "[3/6] Extracting archive..." -ForegroundColor Yellow
    Expand-Archive -Path $ZipFile -DestinationPath . -Force
    Write-Host "[+] Extraction completed" -ForegroundColor Green

    # Step 4: Verify files
    Write-Host "[4/6] Verifying extracted files..." -ForegroundColor Yellow
    Set-Location $ExtractDir
    
    $RequiredFiles = @(
        "0-Install-UV-Recommended.bat",
        "0-Install-Traditional-pip.bat",
        "arina_gui.py",
        "arina_cli.py",
        "requirements.txt"
    )
    
    $MissingFiles = @()
    foreach ($file in $RequiredFiles) {
        if (-not (Test-Path $file)) {
            $MissingFiles += $file
        }
    }
    
    if ($MissingFiles.Count -gt 0) {
        Write-Host "[!] Missing files:" -ForegroundColor Red
        $MissingFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
        throw "Required files missing"
    }
    Write-Host "[+] All required files found" -ForegroundColor Green

    # Step 5: Test UV installation
    Write-Host "[5/6] Testing UV installation..." -ForegroundColor Yellow
    
    # Check if UV is available
    try {
        $uvVersion = & uv --version 2>$null
        Write-Host "[+] UV found: $uvVersion" -ForegroundColor Green
        
        # Run installation script in background
        Write-Host "Starting UV installation script..." -ForegroundColor Gray
        $process = Start-Process -FilePath "0-Install-UV-Recommended.bat" -PassThru -WindowStyle Hidden
        
        # Wait for virtual environment creation
        $timeout = 300 # 5 minutes
        $elapsed = 0
        while (-not (Test-Path ".venv") -and $elapsed -lt $timeout) {
            Start-Sleep -Seconds 5
            $elapsed += 5
            Write-Host "." -NoNewline -ForegroundColor Gray
        }
        Write-Host ""
        
        if (Test-Path ".venv") {
            Write-Host "[+] Virtual environment created successfully" -ForegroundColor Green
            
            # Check if dependencies were installed
            if (Test-Path ".venv\Lib\site-packages\yt_dlp") {
                Write-Host "[+] Core dependencies installed" -ForegroundColor Green
            } else {
                Write-Host "[!] Dependencies may not be fully installed" -ForegroundColor Yellow
            }
        } else {
            Write-Host "[!] Virtual environment not created within timeout" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "[!] UV not found, skipping UV test" -ForegroundColor Yellow
    }

    # Step 6: Test GUI startup (dry run)
    Write-Host "[6/6] Testing GUI startup capability..." -ForegroundColor Yellow
    
    # Check Python availability
    try {
        $pythonVersion = & python --version 2>$null
        Write-Host "[+] Python found: $pythonVersion" -ForegroundColor Green
        
        # Test import capabilities
        $testScript = @"
try:
    import sys
    print(f"Python: {sys.version}")
    
    # Test core imports
    import yt_dlp
    print("✓ yt-dlp available")
    
    try:
        import PySide6
        print("✓ PySide6 available")
    except ImportError:
        print("✗ PySide6 not available")
    
    print("Import test completed")
except Exception as e:
    print(f"Error: {e}")
"@
        
        if (Test-Path ".venv") {
            Write-Host "Testing with virtual environment..." -ForegroundColor Gray
            & .venv\Scripts\python.exe -c $testScript
        } else {
            Write-Host "Testing with system Python..." -ForegroundColor Gray
            & python -c $testScript
        }
        
    } catch {
        Write-Host "[!] Python not found" -ForegroundColor Red
    }

    # Summary
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Installation Test Summary" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Test Directory: $TestDir\$ExtractDir" -ForegroundColor White
    Write-Host "Virtual Environment: $(if (Test-Path '.venv') { 'Created' } else { 'Not Found' })" -ForegroundColor White
    Write-Host ""
    Write-Host "Manual verification commands:" -ForegroundColor Yellow
    Write-Host "cd `"$TestDir\$ExtractDir`"" -ForegroundColor Gray
    Write-Host "uv run python arina_gui.py" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "[!] Test failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Current location: $(Get-Location)" -ForegroundColor Gray
    exit 1
}

Write-Host "Test completed successfully!" -ForegroundColor Green
