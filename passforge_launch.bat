@echo off
REM ============================================
REM   PassForge - Password Generator CLI
REM   Windows Launcher with Interactive Options
REM ============================================

title PassForge - Password Generator

REM Check Python is installed
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check colorama dependency
python -c "import colorama" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required dependency: colorama
    pip install colorama
)

REM Display Menu
:menu
cls
echo  ==========================================================================
echo                       PASSFORGE - Password Generator CLI
echo  ==========================================================================
echo.
echo  QUICK GENERATE                         ADVANCED / PRESETS
echo  ------------------------------         ----------------------------------
echo  [1] Random Password (16 chars)          [7]  JWT Secret
echo  [2] Random Password (custom)            [8]  UUID Token
echo  [3] Passphrase (4 words)                [9]  WiFi Key
echo  [4] Passphrase (custom)                [10] License Key
echo  [5] Leetspeak Password                 [11] Recovery Codes
echo  [6] PIN Code                           [12] OTP Secret
echo.
echo  PRESET PROFILES (One-Click)            TOOLS ^& SYSTEM
echo  ------------------------------         ----------------------------------
echo  [P1] Strong (32 chars)                 [13] Interactive Mode
echo  [P2] Memorable (Easy Say)              [14] View History
echo  [P3] Developer (40 char)               [15] Show Help
echo  [P4] Web Account (16 chars)            [0]  Exit
echo  [P5] WiFi Key (20 chars)
echo  [P6] License Key (5x5)
echo.
echo  ==========================================================================
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto random_default
if "%choice%"=="2" goto random_custom
if "%choice%"=="3" goto phrase_default
if "%choice%"=="4" goto phrase_custom
if "%choice%"=="5" goto leet
if "%choice%"=="6" goto pin
if "%choice%"=="7" goto jwt
if "%choice%"=="8" goto uuid
if "%choice%"=="9" goto wifi
if "%choice%"=="10" goto license
if "%choice%"=="11" goto recovery
if "%choice%"=="12" goto otp
if "%choice%"=="13" goto interactive
if "%choice%"=="14" goto history
if "%choice%"=="15" goto help
if /i "%choice%"=="P1" goto preset_strong
if /i "%choice%"=="P2" goto preset_memorable
if /i "%choice%"=="P3" goto preset_dev
if /i "%choice%"=="P4" goto preset_web
if /i "%choice%"=="P5" goto preset_wifi
if /i "%choice%"=="P6" goto preset_key
if "%choice%"=="0" goto end
echo Invalid option. Press any key to try again...
pause >nul
goto menu

:random_default
cls
echo.
echo  Random Password (16 characters, all character types)
echo  ====================================================
echo.
python main.py --confirm-copy --show-entropy random -l 16
goto menu

:random_custom
cls
echo.
set /p len="Enter password length (8-128): "
set /p show_entropy="Show entropy analysis? (Y/N): "
if /i "%show_entropy%"=="Y" (
    python main.py --confirm-copy --show-entropy random -l %len%
) else (
    python main.py --confirm-copy random -l %len%
)
goto menu

:phrase_default
cls
echo.
echo  Passphrase (4 words, hyphen-separated)
echo  ======================================
echo.
python main.py --confirm-copy --show-entropy phrase -w 4
goto menu

:phrase_custom
cls
echo.
set /p words="Number of words (3-8): "
set /p sep="Separator (default -): "
set /p cap="Capitalize words? (Y/N): "
if "%sep%"=="" set sep=-
if /i "%cap%"=="Y" (
    python main.py --confirm-copy --show-entropy phrase -w %words% -s %sep% --capitalize
) else (
    python main.py --confirm-copy --show-entropy phrase -w %words% -s %sep%
)
goto menu

:leet
cls
echo.
echo  Leetspeak Password
echo  ==================
echo.
set /p words="Number of words (2-5): "
python main.py --confirm-copy --show-entropy leet -w %words%
goto menu

:pin
cls
echo.
set /p len="PIN length (4-8): "
python main.py --confirm-copy --show-entropy pin -l %len%
goto menu

:jwt
cls
echo.
echo  JWT Secret Generator
echo  ====================
echo.
echo  [1] HS256 (256 bits)
echo  [2] HS384 (384 bits)
echo  [3] HS512 (512 bits)
echo.
set /p bits="Select: "
if "%bits%"=="1" set bits=256
if "%bits%"=="2" set bits=384
if "%bits%"=="3" set bits=512
python main.py --confirm-copy --show-entropy jwt --bits %bits%
goto menu

:uuid
cls
echo.
echo  UUID v4 Token
echo  =============
echo.
python main.py --confirm-copy --show-entropy uuid
goto menu

:wifi
cls
echo.
set /p len="WiFi key length (8-63): "
set /p simple="Simple mode (alphanumeric only)? (Y/N): "
if /i "%simple%"=="Y" (
    python main.py --confirm-copy --show-entropy wifi -l %len% --simple
) else (
    python main.py --confirm-copy --show-entropy wifi -l %len%
)
goto menu

:license
cls
echo.
echo  License Key Generator
echo  =====================
echo.
python main.py --confirm-copy --show-entropy license --segments 4 --segment-length 4
goto menu

:recovery
cls
echo.
set /p count="Number of recovery codes (6-12): "
set /p words="Word-based codes? (Y/N): "
if /i "%words%"=="Y" (
    python main.py --confirm-copy recovery -n %count% --words
) else (
    python main.py --confirm-copy recovery -n %count%
)
goto menu

:otp
cls
echo.
echo  OTP Secret (for 2FA apps)
echo  =========================
echo.
python main.py --confirm-copy --show-entropy otp
goto menu

:interactive
cls
python main.py --confirm-copy --interactive
goto menu

:history
cls
echo.
set /p num="Show last N entries (default 10): "
if "%num%"=="" set num=10
python main.py history --last %num%
echo.
pause
goto menu

:help
cls
python main.py --help
echo.
pause
goto menu

:preset_strong
cls
echo.
echo  Preset: STRONG (32 chars, max security)
echo  =========================================
echo.
python main.py --confirm-copy --preset strong --show-entropy
goto menu

:preset_memorable
cls
echo.
echo  Preset: MEMORABLE (easy to say)
echo  =================================
echo.
python main.py --confirm-copy --preset memorable --show-entropy
goto menu

:preset_dev
cls
echo.
echo  Preset: DEVELOPER (40 char alphanumeric)
echo  =========================================
echo.
python main.py --confirm-copy --preset dev --show-entropy
goto menu

:preset_web
cls
echo.
echo  Preset: WEB ACCOUNT (16 chars mixed)
echo  =====================================
echo.
python main.py --confirm-copy --preset web --show-entropy
goto menu

:preset_wifi
cls
echo.
echo  Preset: WIFI KEY (20 chars)
echo  ============================
echo.
python main.py --confirm-copy --preset wifi --show-entropy
goto menu

:preset_key
cls
echo.
echo  Preset: LICENSE KEY (5x5 format)
echo  =================================
echo.
python main.py --confirm-copy --preset key --show-entropy
goto menu

:end
echo.
echo Goodbye!
exit /b 0
