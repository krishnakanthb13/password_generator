@echo off
setlocal enabledelayedexpansion

:: PassForge PWA Launcher for Windows
:: This script starts the local FastAPI server and opens the browser.

echo.
echo  +=========================================+
echo  ^|         PassForge Web Interface         ^|
echo  +=========================================+
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Kill any existing process on port 8093 to avoid bind errors
echo [1/3] Checking for existing PWA processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8093.*LISTENING"') do taskkill /f /pid %%a >nul 2>&1
:: Check for dependencies
echo [2/3] Verifying dependencies...
python -c "import fastapi, uvicorn, multipart" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Missing PWA dependencies. Installing...
    pip install fastapi uvicorn python-multipart
    if !errorlevel! neq 0 (
        echo [ERR] Failed to install dependencies.
        echo Please try manual install: pip install fastapi uvicorn python-multipart
        pause
        exit /b 1
    )
)

:: Open browser in a separate detached process after a short delay
start "" /min cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8093"

:: Start the server in the foreground
echo [3/3] Starting PassForge Web Server...
echo [INFO] Press Ctrl+C to stop the server.
python -m uvicorn pwa.server:app --host 127.0.0.1 --port 8093 --log-level warning

:: When uvicorn exits
echo.
echo [INFO] Server stopped.
pause
