@echo off
REM Process AI Employee Files with Qwen - Auto Approve Mode
REM This runs Qwen with automatic file operation approval

echo ============================================================
echo   AI Employee - Processing Files with Qwen
echo ============================================================
echo.

cd AI_Employee_Vault

echo Running Qwen with auto-approve for file operations...
echo.

REM Use -y flag for YOLO mode (auto-approve)
qwen -y "You are the AI Employee. Process all files in /Needs_Action folder:

1. Read each action file
2. Read Company_Handbook.md for rules
3. For each file:
   - Determine the type and priority
   - Take appropriate actions based on Handbook
   - Update Dashboard.md with activity
   - Create log entry in /Logs/2026-03-31.md
4. Move processed files to /Done/

Report what you processed and what actions you took."

echo.
echo ============================================================
echo   Processing Complete!
echo ============================================================
echo.
echo Check these files for results:
echo   - Dashboard.md (updated activity)
echo   - Logs/2026-03-31.md (action logs)
echo   - Done/ folder (processed files)
echo.
pause
