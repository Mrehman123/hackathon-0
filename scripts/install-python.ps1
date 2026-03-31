# Python Installation Script for AI Employee
# Run this script to install Python automatically

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  Python Installation for AI Employee" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check if Python is already installed
try {
    $pythonPath = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonPath) {
        $version = & python --version
        Write-Host "Python is already installed: $version" -ForegroundColor Green
        Write-Host "No installation needed!" -ForegroundColor Green
        exit 0
    }
} catch {
    # Python not found, continue with installation
}

Write-Host "Python not found. Installing Python..." -ForegroundColor Yellow

# Download Python installer
$pythonVersion = "3.13.2"
$installerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-${pythonVersion}-amd64.exe"
$installerPath = "$env:TEMP\python-installer.exe"

Write-Host "`nDownloading Python $pythonVersion..." -ForegroundColor Cyan
Write-Host "URL: $installerUrl" -ForegroundColor Gray

try {
    # Download the installer
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "Download complete!" -ForegroundColor Green
} catch {
    Write-Host "Download failed: $_" -ForegroundColor Red
    Write-Host "`nPlease install Python manually:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://python.org/downloads/" -ForegroundColor White
    Write-Host "2. Download Python 3.13 or higher" -ForegroundColor White
    Write-Host "3. Run the installer" -ForegroundColor White
    Write-Host "4. CHECK 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    Write-Host "5. Restart your terminal" -ForegroundColor White
    exit 1
}

Write-Host "`nInstalling Python..." -ForegroundColor Cyan

# Run the installer silently with PATH added
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = $installerPath
$processInfo.Arguments = "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0"
$processInfo.UseShellExecute = $false
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true

$process = [System.Diagnostics.Process]::Start($processInfo)
$process.WaitForExit()

if ($process.ExitCode -eq 0) {
    Write-Host "Python installed successfully!" -ForegroundColor Green
    
    # Clean up installer
    Remove-Item $installerPath -Force
    
    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host "  IMPORTANT: Restart your terminal!" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host @"

After restarting your terminal, run:

  cd scripts
  pip install -r requirements.txt

Then test with:

  python test_bronze_tier.py

"@
    Write-Host "============================================================`n" -ForegroundColor Cyan
    
} else {
    Write-Host "Installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
    Write-Host "`nPlease install Python manually from:" -ForegroundColor Yellow
    Write-Host "https://python.org/downloads/" -ForegroundColor White
}
