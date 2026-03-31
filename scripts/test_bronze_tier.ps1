# Bronze Tier Test Script - PowerShell
# Personal AI Employee Hackathon 2026

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  BRONZE TIER TEST SUITE" -ForegroundColor Cyan
Write-Host "  Personal AI Employee Hackathon 2026" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

$vaultPath = "AI_Employee_Vault"
$allPassed = $true

# TEST 1: Vault Structure
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "TEST 1: Vault Structure" -ForegroundColor Cyan
Write-Host "============================================================`n"

$requiredFolders = @(
    "Inbox", "Needs_Action", "Done", "Plans", 
    "Pending_Approval", "Approved", "Rejected", 
    "Logs", "Briefings", "Accounting", "Invoices"
)

$requiredFiles = @(
    "Dashboard.md",
    "Company_Handbook.md", 
    "Business_Goals.md"
)

Write-Host "Checking folders..." -ForegroundColor Yellow
foreach ($folder in $requiredFolders) {
    $folderPath = Join-Path $vaultPath $folder
    if (Test-Path $folderPath -PathType Container) {
        Write-Host "  [OK] /$folder" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] /$folder - MISSING" -ForegroundColor Red
        $allPassed = $false
    }
}

Write-Host "`nChecking files..." -ForegroundColor Yellow
foreach ($file in $requiredFiles) {
    $filePath = Join-Path $vaultPath $file
    if (Test-Path $filePath) {
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $file - MISSING" -ForegroundColor Red
        $allPassed = $false
    }
}

# TEST 2: Create Drop Folder and Test File
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 2: Drop File Test" -ForegroundColor Cyan
Write-Host "============================================================`n"

$dropFolder = Join-Path $vaultPath "Inbox\Drop"
if (-not (Test-Path $dropFolder)) {
    New-Item -ItemType Directory -Path $dropFolder -Force | Out-Null
    Write-Host "  [OK] Created Drop folder" -ForegroundColor Green
} else {
    Write-Host "  [OK] Drop folder exists" -ForegroundColor Green
}

# Create test file
$testFile = Join-Path $dropFolder "test_document.txt"
$testContent = @"
This is a test document for the AI Employee.

Please review this document and:
1. Summarize the contents
2. Categorize it appropriately
3. Suggest any follow-up actions

This is urgent - please process ASAP.
"@

Set-Content -Path $testFile -Value $testContent -Encoding UTF8
Write-Host "  [OK] Created test file: test_document.txt" -ForegroundColor Green

# Create Files folder
$filesFolder = Join-Path $vaultPath "Files"
if (-not (Test-Path $filesFolder)) {
    New-Item -ItemType Directory -Path $filesFolder -Force | Out-Null
    Write-Host "  [OK] Created Files folder" -ForegroundColor Green
}

# Copy test file to Files folder
Copy-Item $testFile (Join-Path $filesFolder "test_document.txt") -Force
Write-Host "  [OK] Copied test file to Files folder" -ForegroundColor Green

# Create action file manually
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$actionFileName = "FILE_test_document_$timestamp.md"
$actionFilePath = Join-Path "$vaultPath\Needs_Action" $actionFileName

$actionContent = @"
---
type: file_drop
source: filesystem
received: $(Get-Date -Format o)
priority: high
status: pending
---

# File Drop for Processing

## File Information
- **Original Name:** test_document.txt
- **Size:** 0.3 KB
- **Location:** Files/test_document.txt
- **Received:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## Suggested Actions
- [ ] Review file contents
- [ ] Categorize file type
- [ ] Take appropriate action based on Company Handbook
- [ ] Move to /Done when complete

## Notes
Add your processing notes here:

"@

Set-Content -Path $actionFilePath -Value $actionContent -Encoding UTF8
Write-Host "  [OK] Created action file: $actionFileName" -ForegroundColor Green

# Remove from drop folder
Remove-Item $testFile -Force
Write-Host "  [OK] Removed from drop folder" -ForegroundColor Green

# TEST 3: Check Scripts
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 3: Scripts Check" -ForegroundColor Cyan
Write-Host "============================================================`n"

$requiredScripts = @(
    "base_watcher.py",
    "filesystem_watcher.py",
    "orchestrator.py",
    "requirements.txt"
)

foreach ($script in $requiredScripts) {
    $scriptPath = Join-Path "scripts" $script
    if (Test-Path $scriptPath) {
        Write-Host "  [OK] $script" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $script - MISSING" -ForegroundColor Red
        $allPassed = $false
    }
}

# TEST 4: Check Qwen Code
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 4: Qwen Code Check" -ForegroundColor Cyan
Write-Host "============================================================`n"

try {
    $qwenVersion = & qwen --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Qwen Code installed: $qwenVersion" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Qwen Code not found" -ForegroundColor Yellow
        Write-Host "         Install with: npm install -g @anthropic/qwen-code" -ForegroundColor Gray
    }
} catch {
    Write-Host "  [WARN] Qwen Code not found" -ForegroundColor Yellow
    Write-Host "         Install with: npm install -g @anthropic/qwen-code" -ForegroundColor Gray
}

# TEST 5: Check Python
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 5: Python Check" -ForegroundColor Cyan
Write-Host "============================================================`n"

try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Python installed: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Python not found" -ForegroundColor Yellow
        Write-Host "         Install from: https://python.org/downloads/" -ForegroundColor Gray
    }
} catch {
    Write-Host "  [WARN] Python not found" -ForegroundColor Yellow
    Write-Host "         Install from: https://python.org/downloads/" -ForegroundColor Gray
}

# SUMMARY
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================`n"

if ($allPassed) {
    Write-Host "  [PASS] All file structure tests passed!" -ForegroundColor Green
    Write-Host "`n  Bronze Tier is READY!" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Some tests failed. Please fix the issues above." -ForegroundColor Red
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS TO TEST" -ForegroundColor Cyan
Write-Host "============================================================"
Write-Host @"

1. Install Python (if not installed):
   Download from: https://python.org/downloads/

2. Install dependencies:
   cd scripts
   pip install -r requirements.txt

3. Run the File Watcher:
   cd scripts
   python filesystem_watcher.py ../AI_Employee_Vault

4. Run the Orchestrator (new terminal):
   cd scripts
   python orchestrator.py ../AI_Employee_Vault

5. Test by dropping a file:
   Copy any file to: AI_Employee_Vault\Inbox\Drop\

6. OR test manually with Qwen:
   cd AI_Employee_Vault
   qwen "Process all files in /Needs_Action"

"@
Write-Host "============================================================`n" -ForegroundColor Cyan
