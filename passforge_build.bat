@echo off
REM PassForge Build Script - Creates standalone executable using PyInstaller
setlocal enabledelayedexpansion

echo ============================================
echo   PassForge Build Script
echo ============================================
echo.

REM Check if PyInstaller is installed
call pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    call pip install pyinstaller
)

echo.
echo Building PassForge executable...
echo.

REM Build the executable
call pyinstaller --onefile ^
    --clean ^
    --name passforge_v1.2.0 ^
    --console ^
    --add-data "src;src" ^
    --hidden-import colorama ^
    --hidden-import json ^
    --hidden-import secrets ^
    --hidden-import base64 ^
    --hidden-import math ^
    --hidden-import uuid ^
    --hidden-import cryptography ^
    --hidden-import zxcvbn ^
    --hidden-import qrcode ^
    --hidden-import dotenv ^
    --add-data "data;data" ^
    --icon NONE ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build FAILED!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Step 1: Build Complete!
echo ============================================
echo.

REM Create Release Package
echo Step 2: Creating Release Package...
set VERSION=1.2.0
set RELEASE_NAME=passforge_v%VERSION%
set RELEASE_DIR=dist\%RELEASE_NAME%
set ZIP_FILE=dist\%RELEASE_NAME%.zip
set TAR_FILE=dist\%RELEASE_NAME%.tar.gz

echo Target Directory: %RELEASE_DIR%

if exist %RELEASE_DIR% rd /s /q %RELEASE_DIR%
mkdir %RELEASE_DIR%

echo Copying artifacts...
copy dist\passforge_v1.2.0.exe "%RELEASE_DIR%\" >nul
copy README.md "%RELEASE_DIR%\" >nul
copy LICENSE "%RELEASE_DIR%\" >nul
copy passforge.example.json "%RELEASE_DIR%\" >nul
copy .example.env "%RELEASE_DIR%\" >nul
copy passforge_quick.bat "%RELEASE_DIR%\" >nul
copy passforge_launch.bat "%RELEASE_DIR%\" >nul
copy passforge_pwa.bat "%RELEASE_DIR%\" >nul
copy DESIGN_PHILOSOPHY.md "%RELEASE_DIR%\" >nul
copy CODE_DOCUMENTATION.md "%RELEASE_DIR%\" >nul
copy SECURITY.md "%RELEASE_DIR%\" >nul
copy RELEASE_NOTES.md "%RELEASE_DIR%\" >nul
xcopy /E /I /Y data "%RELEASE_DIR%\data" >nul
xcopy /E /I /Y pwa "%RELEASE_DIR%\pwa" >nul

if errorlevel 1 (
    echo [ERROR] Failed to copy files to release directory.
    pause
    exit /b 1
)

echo.
echo Step 3: Packaging as ZIP...
if exist "%ZIP_FILE%" del /f /q "%ZIP_FILE%"
powershell -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_FILE%' -Force"

echo.
echo Step 4: Packaging as tar.gz...
if exist "%TAR_FILE%" del /f /q "%TAR_FILE%"
REM Use Windows built-in tar command
tar -czf "%TAR_FILE%" -C dist "%RELEASE_NAME%"

if errorlevel 1 (
    echo [WARNING] tar.gz packaging failed (requires modern Windows 10/11^).
)

echo.
echo ============================================
echo   Build and Packaging Successful!
echo ============================================
echo.
echo Binary:   dist\passforge_v1.2.0.exe
echo Folder:   %RELEASE_DIR%\
echo ZIP:      dist\passforge_v1.2.0.zip
echo TAR.GZ:   dist\passforge_v1.2.0.tar.gz
echo.

REM Test the executable
echo Testing the binary...
dist\passforge_v1.2.0.exe --version
dist\passforge_v1.2.0.exe random -l 12

echo.
echo Process complete!
pause
endlocal
