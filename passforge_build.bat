@echo off
REM PassForge Build Script - Creates standalone executable using PyInstaller

echo ============================================
echo   PassForge Build Script
echo ============================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building PassForge executable...
echo.

REM Build the executable
pyinstaller --onefile ^
    --name passforge ^
    --console ^
    --add-data "src;src" ^
    --hidden-import colorama ^
    --hidden-import json ^
    --hidden-import secrets ^
    --hidden-import base64 ^
    --hidden-import math ^
    --hidden-import uuid ^
    --icon NONE ^
    main.py

if errorlevel 1 (
    echo.
    echo Build FAILED!
    exit /b 1
)

echo.
echo ============================================
echo   Build Complete!
echo ============================================
echo.
echo Executable location: dist\passforge.exe
echo.

REM Test the executable
echo Testing the executable...
dist\passforge.exe --version
dist\passforge.exe random -l 12

echo.
echo Build successful!
pause
