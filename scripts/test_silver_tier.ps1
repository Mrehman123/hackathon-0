# Silver Tier Test Script
# Tests all Silver Tier components

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  SILVER TIER TEST SUITE" -ForegroundColor Cyan
Write-Host "  Personal AI Employee Hackathon 2026" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

$allPassed = $true
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','User')

# TEST 1: Python Dependencies
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "TEST 1: Python Dependencies" -ForegroundColor Cyan
Write-Host "============================================================`n"

$pythonDeps = @(
    'watchdog',
    'googleapiclient',
    'google_auth_oauthlib',
    'playwright',
    'linkedin_api',
    'requests',
    'dotenv',
    'schedule',
    'apscheduler'
)

foreach ($dep in $pythonDeps) {
    try {
        $result = python -c "import $dep; print($dep.__version__ if hasattr($dep, '__version__') else 'OK')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] $dep" -ForegroundColor Green
        } else {
            Write-Host "  [FAIL] $dep - $result" -ForegroundColor Red
            $allPassed = $false
        }
    } catch {
        Write-Host "  [FAIL] $dep" -ForegroundColor Red
        $allPassed = $false
    }
}

# TEST 2: Node.js and MCP Dependencies
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 2: Node.js and MCP Dependencies" -ForegroundColor Cyan
Write-Host "============================================================`n"

try {
    $nodeVersion = node --version 2>&1
    Write-Host "  [OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Node.js not found" -ForegroundColor Red
    $allPassed = $false
}

try {
    $npmVersion = npm --version 2>&1
    Write-Host "  [OK] npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] npm not found" -ForegroundColor Red
    $allPassed = $false
}

# Check MCP servers
$mcpServers = @('linkedin-mcp', 'email-mcp')
foreach ($server in $mcpServers) {
    $packagePath = "mcp-servers\$server\package.json"
    $nodeModules = "mcp-servers\$server\node_modules"
    
    if (Test-Path $packagePath) {
        Write-Host "  [OK] $server package.json exists" -ForegroundColor Green
        if (Test-Path $nodeModules) {
            Write-Host "  [OK] $server dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "  [WARN] $server dependencies not installed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [FAIL] $server not found" -ForegroundColor Red
        $allPassed = $false
    }
}

# TEST 3: Watcher Scripts
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 3: Watcher Scripts" -ForegroundColor Cyan
Write-Host "============================================================`n"

$watcherScripts = @(
    'base_watcher.py',
    'filesystem_watcher.py',
    'gmail_watcher.py',
    'whatsapp_watcher.py',
    'orchestrator.py',
    'approval_handler.py',
    'scheduler.py'
)

foreach ($script in $watcherScripts) {
    $scriptPath = "scripts\$script"
    if (Test-Path $scriptPath) {
        Write-Host "  [OK] $script" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $script - MISSING" -ForegroundColor Red
        $allPassed = $false
    }
}

# TEST 4: Vault Structure
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 4: Vault Structure" -ForegroundColor Cyan
Write-Host "============================================================`n"

$vaultFolders = @(
    'Briefings',
    'Accounting',
    'Inbox/Drop',
    'Needs_Action',
    'Pending_Approval',
    'Approved',
    'Rejected',
    'Done',
    'Logs'
)

foreach ($folder in $vaultFolders) {
    $folderPath = "AI_Employee_Vault\$folder"
    if (Test-Path $folderPath) {
        Write-Host "  [OK] /$folder" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] /$folder - MISSING" -ForegroundColor Red
        $allPassed = $false
        # Create missing folder
        New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
        Write-Host "  [INFO] Created /$folder" -ForegroundColor Gray
    }
}

# TEST 5: Qwen Code
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 5: Qwen Code" -ForegroundColor Cyan
Write-Host "============================================================`n"

try {
    $qwenVersion = qwen --version 2>&1
    Write-Host "  [OK] Qwen Code: $qwenVersion" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] Qwen Code not found" -ForegroundColor Yellow
    Write-Host "         Install: npm install -g @anthropic/qwen-code" -ForegroundColor Gray
}

# TEST 6: Playwright Browsers
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 6: Playwright Browsers" -ForegroundColor Cyan
Write-Host "============================================================`n"

try {
    $pwResult = playwright --version 2>&1
    Write-Host "  [OK] Playwright installed" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Playwright not installed" -ForegroundColor Red
    Write-Host "         Run: playwright install" -ForegroundColor Gray
    $allPassed = $false
}

# TEST 7: Environment File
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST 7: Environment Configuration" -ForegroundColor Cyan
Write-Host "============================================================`n"

$envFile = "scripts\.env"
$envExample = "scripts\.env.example"

if (Test-Path $envFile) {
    Write-Host "  [OK] .env file exists" -ForegroundColor Green
} else {
    Write-Host "  [INFO] .env file not found" -ForegroundColor Yellow
    Write-Host "         Copy .env.example to .env and configure" -ForegroundColor Gray
}

if (Test-Path $envExample) {
    Write-Host "  [OK] .env.example template exists" -ForegroundColor Green
} else {
    Write-Host "  [WARN] .env.example not found" -ForegroundColor Yellow
}

# SUMMARY
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================`n"

if ($allPassed) {
    Write-Host "  [PASS] All critical tests passed!" -ForegroundColor Green
    Write-Host "`n  Silver Tier is READY!" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Some tests failed. Review the output above." -ForegroundColor Yellow
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "============================================================"
Write-Host @"

1. Configure environment:
   cd scripts
   copy .env.example .env
   # Edit .env with your credentials

2. Set up Gmail API:
   - Visit: https://developers.google.com/gmail/api/quickstart/python
   - Download credentials.json to scripts/

3. Set up LinkedIn:
   - Visit: https://www.linkedin.com/developers/apps
   - Create app and get access token

4. Test watchers:
   cd scripts
   python filesystem_watcher.py ../AI_Employee_Vault

5. Test with Qwen:
   cd AI_Employee_Vault
   qwen "Process files in Needs_Action"

"@
Write-Host "============================================================`n" -ForegroundColor Cyan
