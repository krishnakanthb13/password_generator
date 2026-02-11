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
echo                 PASSFORGE - Password Generator CLI v1.1.6
echo  ==========================================================================
echo.
echo  QUICK GENERATE                         ADVANCED / PRESETS
echo  ------------------------------         ----------------------------------
echo  [1] Random Password (16 chars)          [8]  JWT Secret
echo  [2] Random Password (custom)            [9]  UUID Token
echo  [3] Passphrase (4 words)               [10] WiFi Key
echo  [4] Passphrase (custom)                [11] License Key
echo  [5] Themed Passphrase                  [12] Recovery Codes
echo  [6] Leetspeak Password                 [13] OTP Secret
echo  [7] PIN Code

echo.
echo  PRESET PROFILES (One-Click)            TOOLS ^& SYSTEM
echo  ------------------------------         ----------------------------------
echo  [P1] Strong (32 chars)                 [14] Interactive Mode
echo  [P2] Memorable (Easy Say)              [15] NATO Phonetic
echo  [P3] Developer (40 char)               [16] View History
echo  [P4] Web Account (16 chars)            [17] Show Help
echo  [P5] WiFi Key (20 chars)               [18] Paranoid Mode
echo  [P6] License Key (5x5)                 [19] Base64 Secret
echo  [0]  Exit                              [20] Pronounceable
echo.
echo  ==========================================================================
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto random_default
if "%choice%"=="2" goto random_custom
if "%choice%"=="3" goto phrase_default
if "%choice%"=="4" goto phrase_custom
if "%choice%"=="5" goto themed_phrase
if "%choice%"=="6" goto leet
if "%choice%"=="7" goto pin
if "%choice%"=="8" goto jwt
if "%choice%"=="9" goto uuid
if "%choice%"=="10" goto wifi
if "%choice%"=="11" goto license
if "%choice%"=="12" goto recovery
if "%choice%"=="13" goto otp
if "%choice%"=="14" goto interactive
if "%choice%"=="15" goto phonetic
if "%choice%"=="16" goto history
if "%choice%"=="17" goto help
if "%choice%"=="18" goto paranoid
if "%choice%"=="19" goto base64
if "%choice%"=="20" goto pronounceable
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
python main.py --log --confirm-copy --show-entropy random -l 16
goto menu

:random_custom
cls
echo.
echo  Random Password (custom length)
echo  ===============================
echo.
call :read_int "Password length (4-1024)" 16 4 1024 len
python main.py --log --confirm-copy --show-entropy random -l %len%
goto menu

:phrase_default
cls
echo.
echo  Passphrase (4 words, hyphen-separated)
echo  ======================================
python main.py --log --confirm-copy --show-entropy phrase -w 4
goto menu

:phrase_custom
cls
echo.
echo  Passphrase (custom settings)
echo  ============================
echo.
call :read_int "Number of words (2-64)" 4 2 64 words
set /p style="Style: [N]one, [C]apitalize, [S]nake_case, [A]lternate, [U]ppercase [N]: "
if /i "%style%"=="S" (
    set sep=_
) else (
    echo Suggested separators: - _ . / \ +
    set "sep=-"
    set /p sep="Separator (default -): "
)
if /i "%style%"=="C" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep% --capitalize
) else if /i "%style%"=="S" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s _
) else if /i "%style%"=="A" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep% --alternate
) else if /i "%style%"=="U" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep% --uppercase
) else (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep%
)
goto menu

:themed_phrase
cls
echo.
echo  Themed Passphrase
echo  =================
echo.
echo  Available Themes:
echo  -----------------
setlocal enabledelayedexpansion
set "i=1"
for %%f in (data\wordlists\*.txt) do (
    echo  [!i!] %%~nf
    set "theme_!i!=%%~nf"
    set /a i+=1
)
set /a count=i-1
echo.
call :read_int "Select theme number" 1 1 %count% choice
set theme=!theme_%choice%!
endlocal & set theme=%theme%

echo.
echo  Selected: %theme%
echo.
call :read_int "Number of words (2-64)" 4 2 64 words
set /p style="Style: [N]one, [C]apitalize, [S]nake_case, [A]lternate, [U]ppercase [N]: "
if /i "%style%"=="S" (
    set sep=_
) else (
    echo Suggested separators: - _ . / \ +
    set "sep=-"
    set /p sep="Separator (default -): "
)
if /i "%style%"=="C" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep% --capitalize --wordlist "data\wordlists\%theme%.txt"
) else if /i "%style%"=="S" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s _ --wordlist "data\wordlists\%theme%.txt"
) else if /i "%style%"=="A" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep% --alternate --wordlist "data\wordlists\%theme%.txt"
) else if /i "%style%"=="U" (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep% --uppercase --wordlist "data\wordlists\%theme%.txt"
) else (
    python main.py --log --confirm-copy --show-entropy phrase -w %words% -s %sep% --wordlist "data\wordlists\%theme%.txt"
)
goto menu

:leet
cls
echo.
echo  Leetspeak Password
echo  ==================
echo.
call :read_int "Number of words (2-64)" 3 2 64 words
python main.py --log --confirm-copy --show-entropy leet -w %words%
goto menu

:pin
cls
echo.
echo  PIN Generator
echo  =============
echo.
call :read_int "PIN length (4-64)" 6 4 64 len
python main.py --log --confirm-copy --show-entropy pin -l %len%
goto menu

:pronounceable
cls
echo.
echo  Pronounceable Password
echo  ======================
echo.
call :read_int "Password length (4-128)" 12 4 128 len
python main.py --log --confirm-copy --show-entropy pronounce -l %len%
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
call :read_int "Select algorithm" 1 1 3 bits
if "%bits%"=="1" set bits=256
if "%bits%"=="2" set bits=384
if "%bits%"=="3" set bits=512
python main.py --log --confirm-copy --show-entropy jwt --bits %bits%
goto menu

:uuid
cls
echo.
echo  UUID v4 Token
echo  =============
python main.py --log --confirm-copy --show-entropy uuid
goto menu

:wifi
cls
echo.
echo  WiFi Key Generator
echo  ==================
echo.
call :read_int "WiFi key length (8-63)" 24 8 63 len
set /p simple="Simple mode (alphanumeric only)? (Y/N) [N]: "
if /i "%simple%"=="Y" (
    python main.py --log --confirm-copy --show-entropy wifi -l %len% --simple
) else (
    python main.py --log --confirm-copy --show-entropy wifi -l %len%
)
goto menu

:license
cls
echo.
echo  License Key Generator (AXB)
echo  ===========================
echo.
call :read_int "Number of segments (2-64)" 5 2 64 segments
call :read_int "Segment length (2-32)" 5 2 32 length
echo.
python main.py --log --confirm-copy --show-entropy license --segments %segments% --segment-length %length%
goto menu

:recovery
cls
echo.
echo  Recovery Codes
echo  ==============
echo.
call :read_int "Number of codes (5-100)" 8 5 100 count
set /p words="Word-based codes? (Y/N) [N]: "
if /i "%words%"=="Y" (
    python main.py --log --confirm-copy --show-entropy recovery -n %count% --words
) else (
    python main.py --log --confirm-copy --show-entropy recovery -n %count%
)
goto menu

:otp
cls
echo.
echo  OTP Secret (for 2FA apps)
echo  =========================
python main.py --log --confirm-copy --show-entropy otp
goto menu

:base64
cls
echo.
echo  Base64 Secret Generator
echo  =======================
echo.
call :read_int "Number of bytes (8-1024)" 32 8 1024 byt
python main.py --log --confirm-copy --show-entropy base64 -b %byt%
goto menu

:interactive
cls
echo.
echo  Interactive Mode
echo  ================
python main.py --log --confirm-copy --interactive
goto menu

:phonetic
cls
echo.
echo  NATO Phonetic Alphabet
echo  ======================
echo.
set /p text="Text to convert (leave empty for random): "
if "%text%"=="" (
    call :read_int "Random length (4-128)" 8 4 128 len
    python main.py --log --confirm-copy phonetic -l %len%
) else (
    python main.py --log --confirm-copy phonetic --text "%text%"
)
goto menu

:history
cls
echo.
echo  Generation History
echo  ==================
call :read_int "Show last N entries (1-100)" 10 1 100 num
python main.py history --last %num%
echo.
pause
goto menu

:help
cls
echo.
echo  Command Line Help
echo  =================
python main.py --help
echo.
pause
goto menu

:paranoid
cls
echo.
echo  Paranoid Mode (High-Security Generator)
echo  =======================================
python main.py --log --confirm-copy --show-entropy --paranoid random -l 32
goto menu

:preset_strong
cls
echo.
echo  Preset: STRONG (32 chars, max security)
echo  =========================================
python main.py --log --confirm-copy --preset strong --show-entropy
goto menu

:preset_memorable
cls
echo.
echo  Preset: MEMORABLE (easy to say)
echo  =================================
python main.py --log --confirm-copy --preset memorable --show-entropy
goto menu

:preset_dev
cls
echo.
echo  Preset: DEVELOPER (40 char alphanumeric)
echo  =========================================
python main.py --log --confirm-copy --preset dev --show-entropy
goto menu

:preset_web
cls
echo.
echo  Preset: WEB ACCOUNT (16 chars mixed)
echo  =====================================
python main.py --log --confirm-copy --preset web --show-entropy
goto menu

:preset_wifi
cls
echo.
echo  Preset: WIFI KEY (20 chars)
echo  ============================
python main.py --log --confirm-copy --preset wifi --show-entropy
goto menu

:preset_key
cls
echo.
echo  Preset: LICENSE KEY (5x5 format)
echo  =================================
python main.py --log --confirm-copy --preset key --show-entropy
goto menu

:read_int
REM %1=prompt, %2=default, %3=min, %4=max, %5=varname
set "%~5=%~2"
:read_loop
set "input_val=%~2"
set /p "input_val=%~1 [%~2]: "
echo %input_val%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo [Error] Please enter a valid number.
    goto read_loop
)
if %input_val% lss %~3 (
    echo [Error] Value must be at least %~3.
    goto read_loop
)
if %input_val% gtr %~4 (
    echo [Error] Value must be no more than %~4.
    goto read_loop
)
set "%~5=%input_val%"
exit /b

:end
echo.
echo Goodbye!
exit /b 0