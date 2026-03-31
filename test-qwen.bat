@echo off
REM Quick Test Script for AI Employee Bronze Tier
REM This script sets up the correct PATH and runs tests

echo ============================================================
echo   AI Employee Bronze Tier - Quick Test
echo ============================================================
echo.

REM Set Python PATH
set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python313
set PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    goto :end
)
echo.

echo [2/3] Checking watchdog...
pip show watchdog | find "Version"
echo.

echo [3/3] Checking Qwen...
qwen --version
echo.

echo ============================================================
echo   READY TO TEST!
echo ============================================================
echo.
echo To test the AI Employee:
echo.
echo   1. Run this command:
echo      cd AI_Employee_Vault
echo      qwen
echo.
echo   2. When prompted, type: 1
echo.
echo   3. Then paste this prompt:
echo      "Check /Needs_Action folder and process all action files"
echo      "according to Company_Handbook.md. Update Dashboard.md"
echo      "and move completed files to /Done/."
echo.
echo ============================================================
pause

:end
