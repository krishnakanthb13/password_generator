#!/bin/bash
# ============================================
#   PassForge - Password Generator CLI
#   Unix/Linux/macOS Launcher
# ============================================

# Trap signals for graceful shutdown
trap 'echo " Interrupted. Exiting..."; exit 0' SIGINT SIGTERM

# Colors (Bold/Bright for better visibility)
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Python is not installed."
        echo "Please install Python 3.8+ from https://python.org"
        exit 1
    fi
    PYTHON="python"
else
    PYTHON="python3"
fi

# Check colorama
$PYTHON -c "import colorama" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[INFO]${NC} Installing required dependency: colorama"
    pip install colorama || pip3 install colorama
fi

# Helper: Read integer with validation
read_int() {
    local prompt=$1
    local default=$2
    local min=$3
    local max=$4
    local var_name=$5
    local val=""

    while true; do
        read -p "$prompt [$default]: " val
        [[ -z "$val" ]] && val=$default
        if [[ "$val" =~ ^[0-9]+$ ]] && [ "$val" -ge "$min" ] && [ "$val" -le "$max" ]; then
            eval "$var_name=$val"
            break
        else
            echo -e "  ${RED}[Error] Please enter a number between $min and $max.${NC}"
        fi
    done
}

# Display Menu
show_menu() {
    clear
    echo ""
    echo -e "${BLUE}==========================================================================${NC}"
    echo -e "               ${BLUE}PASSFORGE - Password Generator CLI v1.0.14${NC}"
    echo -e "${BLUE}==========================================================================${NC}"
    echo ""
    echo -e "  ${YELLOW}QUICK GENERATE${NC}                         ${YELLOW}ADVANCED / PRESETS${NC}"
    echo -e "  ------------------------------         ----------------------------------"
    echo -e "  [1] Random Password (16 chars)          [8]  JWT Secret"
    echo -e "  [2] Random Password (custom)            [9]  UUID Token"
    echo -e "  [3] Passphrase (4 words)               [10] WiFi Key"
    echo -e "  [4] Passphrase (custom)                [11] License Key"
    echo -e "  [5] Themed Passphrase                  [12] Recovery Codes"
    echo -e "  [6] Leetspeak Password                 [13] OTP Secret"
    echo -e "  [7] PIN Code"
    echo ""
    echo -e "  ${YELLOW}PRESET PROFILES (One-Click)${NC}            ${YELLOW}TOOLS & SYSTEM${NC}"
    echo -e "  ------------------------------         ----------------------------------"
    echo -e "  [P1] Strong (32 chars)                 [14] Interactive Mode"
    echo -e "  [P2] Memorable (Easy Say)              [15] NATO Phonetic"
    echo -e "  [P3] Developer (40 char)               [16] View History"
    echo -e "  [P4] Web Account (16 chars)            [17] Show Help"
    echo -e "  [P5] WiFi Key (20 chars)               [18] Paranoid Mode"
    echo -e "  [P6] License Key (5x5)                 [0]  Exit"
    echo ""
    echo -e "${BLUE}==========================================================================${NC}"
    echo ""
}

pause() {
    echo ""
    read -p "  Press Enter to return to menu..."
}

# Main loop
while true; do
    show_menu
    read -p "Select option: " choice

    case $choice in
        1)
            clear
            echo "Random Password (16 characters)"
            echo "================================"
            $PYTHON main.py --log --confirm-copy --show-entropy random -l 16
            echo ""
            ;;
        2)
            clear
            echo ""
            echo "Random Password (custom length)"
            echo "==============================="
            echo ""
            read_int "Enter password length" 16 8 128 len
            read -p "Show entropy analysis? (y/n) [n]: " show_ent
            if [[ "$show_ent" == "y" || "$show_ent" == "Y" ]]; then
                $PYTHON main.py --log --confirm-copy --show-entropy random -l "$len"
            else
                $PYTHON main.py --log --confirm-copy random -l "$len"
            fi
            echo ""
            ;;
        3)
            clear
            echo "Passphrase (4 words)"
            echo "===================="
            $PYTHON main.py --log --confirm-copy --show-entropy phrase -w 4
            echo ""
            ;;
        4)
            clear
            echo ""
            echo "Passphrase (custom settings)"
            echo "============================"
            echo ""
            read_int "Number of words" 4 3 8 words
            read -p "Separator (default -): " sep
            read -p "Capitalize words? (y/n) [n]: " cap
            [[ -z "$sep" ]] && sep="-"
            if [[ "$cap" == "y" || "$cap" == "Y" ]]; then
                $PYTHON main.py --log --confirm-copy --show-entropy phrase -w "$words" -s "$sep" --capitalize
            else
                $PYTHON main.py --log --confirm-copy --show-entropy phrase -w "$words" -s "$sep"
            fi
            echo ""
            ;;
        5)
            clear
            echo ""
            echo "Themed Passphrase"
            echo "================="
            echo ""
            echo "Available Themes:"
            echo "-----------------"
            i=1
            wordlists=()
            for f in data/wordlists/*.txt; do
                name=$(basename "$f" .txt)
                echo "  [$i] $name"
                wordlists+=("$name")
                i=$((i+1))
            done
            count=${#wordlists[@]}
            
            echo ""
            read_int "Select theme number" 1 1 "$count" choice
            
            # Array index is 0-based
            idx=$((choice-1))
            theme="${wordlists[$idx]}"
            
            echo ""
            echo "Selected: $theme"
            read_int "Number of words" 4 2 12 words
            read -p "Separator (default -): " sep
            [[ -z "$sep" ]] && sep="-"
            read -p "Capitalize words? (y/n) [n]: " cap
            
            if [[ "$cap" == "y" || "$cap" == "Y" ]]; then
                $PYTHON main.py --log --confirm-copy --show-entropy phrase -w "$words" -s "$sep" --capitalize --wordlist "data/wordlists/$theme.txt"
            else
                $PYTHON main.py --log --confirm-copy --show-entropy phrase -w "$words" -s "$sep" --wordlist "data/wordlists/$theme.txt"
            fi
            echo ""
            ;;
        6)
            clear
            echo ""
            echo "Leetspeak Password"
            echo "=================="
            echo ""
            read_int "Number of words" 3 2 5 words
            $PYTHON main.py --log --confirm-copy --show-entropy leet -w "$words"
            echo ""
            ;;
        7)
            clear
            echo ""
            echo "PIN Generator"
            echo "============="
            echo ""
            read_int "PIN length" 6 4 8 len
            $PYTHON main.py --log --confirm-copy --show-entropy pin -l "$len"
            echo ""
            ;;
            echo ""
            $PYTHON main.py --log --confirm-copy --show-entropy pin -l "$len"
            echo ""
            ;;
        8)
            clear
            echo "JWT Secret Generator"
            echo "===================="
            echo " [1] HS256 (256 bits)"
            echo " [2] HS384 (384 bits)"
            echo " [3] HS512 (512 bits)"
            read_int "Select algorithm" 1 1 3 bits_choice
            case $bits_choice in
                1) bits=256 ;;
                2) bits=384 ;;
                3) bits=512 ;;
                *) bits=256 ;;
            esac
            $PYTHON main.py --log --confirm-copy --show-entropy jwt --bits "$bits"
            echo ""
            ;;
        9)
            clear
            echo "UUID v4 Token"
            echo "============="
            $PYTHON main.py --log --confirm-copy --show-entropy uuid
            echo ""
            ;;
        10)
            clear
            echo ""
            echo "WiFi Key Generator"
            echo "=================="
            echo ""
            read_int "WiFi key length" 16 8 63 len
            read -p "Simple mode (alphanumeric only)? (y/n) [n]: " simple
            if [[ "$simple" == "y" || "$simple" == "Y" ]]; then
                $PYTHON main.py --log --confirm-copy --show-entropy wifi -l "$len" --simple
            else
                $PYTHON main.py --log --confirm-copy --show-entropy wifi -l "$len"
            fi
            echo ""
            ;;
        11)
            clear
            echo "License Key Generator (AXB)"
            echo "==========================="
            echo ""
            read_int "Number of segments (A)" 5 2 10 segments
            read_int "Segment length (B)" 5 2 10 length
            echo ""
            $PYTHON main.py --log --confirm-copy --show-entropy license --segments "$segments" --segment-length "$length"
            echo ""
            ;;
        12)
            clear
            echo ""
            echo "Recovery Codes"
            echo "=============="
            echo ""
            read_int "Number of recovery codes" 8 6 12 count
            read -p "Word-based codes? (y/n) [n]: " word_based
            if [[ "$word_based" == "y" || "$word_based" == "Y" ]]; then
                $PYTHON main.py --log --confirm-copy recovery -n "$count" --words
            else
                $PYTHON main.py --log --confirm-copy recovery -n "$count"
            fi
            echo ""
            ;;
        13)
            clear
            echo "OTP Secret (for 2FA apps)"
            echo "========================="
            $PYTHON main.py --log --confirm-copy --show-entropy otp
            echo ""
            ;;
        14)
            clear
            echo "Interactive Mode"
            echo "================"
            $PYTHON main.py --log --confirm-copy --interactive
            ;;
        15)
            clear
            echo "NATO Phonetic Alphabet"
            echo "======================"
            echo ""
            read -p "Text to convert (leave empty for random): " text
            if [[ -z "$text" ]]; then
                read_int "Random length" 8 4 32 len
                $PYTHON main.py --log --confirm-copy phonetic -l "$len"
            else
                $PYTHON main.py --log --confirm-copy phonetic --text "$text"
            fi
            echo ""
            pause
            ;;
        16)
            clear
            echo "Generation History"
            echo "=================="
            read_int "Show last N entries" 10 1 100 num
            [[ -z "$num" ]] && num=10
            $PYTHON main.py --confirm-copy history --last "$num"
            echo ""
            pause
            ;;
        17)
            clear
            echo "Command Line Help"
            echo "================="
            $PYTHON main.py --confirm-copy --help
            echo ""
            pause
            ;;
        18)
            clear
            echo ""
            echo "Paranoid Mode (High-Security Generator)"
            echo "======================================="
            $PYTHON main.py --log --confirm-copy --show-entropy --paranoid random -l 32
            echo ""
            pause
            ;;
        0)
            echo ""
            echo "Goodbye!"
            exit 0
            ;;
        [Pp]1)
            clear
            echo ""
            echo "Preset: STRONG (32 chars, max security)"
            echo "========================================="
            $PYTHON main.py --log --confirm-copy --preset strong --show-entropy
            echo ""
            ;;
        [Pp]2)
            clear
            echo ""
            echo "Preset: MEMORABLE (easy to say)"
            echo "================================="
            $PYTHON main.py --log --confirm-copy --preset memorable --show-entropy
            echo ""
            ;;
        [Pp]3)
            clear
            echo ""
            echo "Preset: DEVELOPER (40 char alphanumeric)"
            echo "========================================="
            $PYTHON main.py --log --confirm-copy --preset dev --show-entropy
            echo ""
            ;;
        [Pp]4)
            clear
            echo ""
            echo "Preset: WEB ACCOUNT (16 chars mixed)"
            echo "====================================="
            $PYTHON main.py --log --confirm-copy --preset web --show-entropy
            echo ""
            ;;
        [Pp]5)
            clear
            echo ""
            echo "Preset: WIFI KEY (20 chars)"
            echo "============================"
            $PYTHON main.py --log --confirm-copy --preset wifi --show-entropy
            echo ""
            ;;
        [Pp]6)
            clear
            echo ""
            echo "Preset: LICENSE KEY (5x5 format)"
            echo "================================="
            $PYTHON main.py --log --confirm-copy --preset key --show-entropy
            echo ""
            ;;
        *)
            echo "Invalid option. Press Enter to try again..."
            read
            ;;
    esac
done
