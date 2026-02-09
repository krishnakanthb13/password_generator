@echo off
REM Quick launcher - generates a random password instantly
REM Usage: Double-click or run from terminal

title PassForge Quick

REM Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install from https://python.org
    pause
    exit /b 1
)

REM Generate password with entropy
python main.py --show-entropy random -l 16
echo.
pause
