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

# Display Menu
show_menu() {
    clear
    echo ""
    echo -e "${BLUE}==========================================================================${NC}"
    echo -e "                     ${BLUE}PASSFORGE - Password Generator CLI${NC}"
    echo -e "${BLUE}==========================================================================${NC}"
    echo ""
    echo -e "  ${YELLOW}QUICK GENERATE${NC}                         ${YELLOW}ADVANCED / PRESETS${NC}"
    echo -e "  ------------------------------         ----------------------------------"
    echo -e "  [1] Random Password (16 chars)          [7]  JWT Secret"
    echo -e "  [2] Random Password (custom)            [8]  UUID Token"
    echo -e "  [3] Passphrase (4 words)                [9]  WiFi Key"
    echo -e "  [4] Passphrase (custom)                [10] License Key"
    echo -e "  [5] Leetspeak Password                 [11] Recovery Codes"
    echo -e "  [6] PIN Code                           [12] OTP Secret"
    echo ""
    echo -e "  ${YELLOW}PRESET PROFILES (One-Click)${NC}            ${YELLOW}TOOLS & SYSTEM${NC}"
    echo -e "  ------------------------------         ----------------------------------"
    echo -e "  [P1] Strong (32 chars)                 [13] Interactive Mode"
    echo -e "  [P2] Memorable (Easy Say)              [14] View History"
    echo -e "  [P3] Developer (40 char)               [15] Show Help"
    echo -e "  [P4] Web Account (16 chars)            [0]  Exit"
    echo -e "  [P5] WiFi Key (20 chars)"
    echo -e "  [P6] License Key (5x5)"
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
            echo ""
            echo "Random Password (16 characters)"
            echo "================================"
            echo ""
            $PYTHON main.py --confirm-copy --show-entropy random -l 16
            echo ""
            ;;
        2)
            clear
            read -p "Enter password length (8-128): " len
            read -p "Show entropy analysis? (y/n): " show_ent
            if [[ "$show_ent" == "y" || "$show_ent" == "Y" ]]; then
                $PYTHON main.py --confirm-copy --show-entropy random -l "$len"
            else
                $PYTHON main.py --confirm-copy random -l "$len"
            fi
            echo ""
            ;;
        3)
            clear
            echo ""
            echo "Passphrase (4 words)"
            echo "===================="
            echo ""
            $PYTHON main.py --confirm-copy --show-entropy phrase -w 4
            echo ""
            ;;
        4)
            clear
            read -p "Number of words (3-8): " words
            read -p "Separator (default -): " sep
            read -p "Capitalize words? (y/n): " cap
            [[ -z "$sep" ]] && sep="-"
            if [[ "$cap" == "y" || "$cap" == "Y" ]]; then
                $PYTHON main.py --confirm-copy --show-entropy phrase -w "$words" -s "$sep" --capitalize
            else
                $PYTHON main.py --confirm-copy --show-entropy phrase -w "$words" -s "$sep"
            fi
            echo ""
            ;;
        5)
            clear
            read -p "Number of words (2-5): " words
            $PYTHON main.py --confirm-copy --show-entropy leet -w "$words"
            echo ""
            ;;
        6)
            clear
            read -p "PIN length (4-8): " len
            $PYTHON main.py --confirm-copy --show-entropy pin -l "$len"
            echo ""
            ;;
        7)
            clear
            echo ""
            echo "JWT Secret Generator"
            echo "===================="
            echo " [1] HS256 (256 bits)"
            echo " [2] HS384 (384 bits)"
            echo " [3] HS512 (512 bits)"
            echo ""
            read -p "Select: " bits_choice
            case $bits_choice in
                1) bits=256 ;;
                2) bits=384 ;;
                3) bits=512 ;;
                *) bits=256 ;;
            esac
            $PYTHON main.py --confirm-copy --show-entropy jwt --bits "$bits"
            echo ""
            ;;
        8)
            clear
            echo ""
            echo "UUID v4 Token"
            echo "============="
            echo ""
            $PYTHON main.py --confirm-copy --show-entropy uuid
            echo ""
            ;;
        9)
            clear
            read -p "WiFi key length (8-63): " len
            read -p "Simple mode (alphanumeric only)? (y/n): " simple
            if [[ "$simple" == "y" || "$simple" == "Y" ]]; then
                $PYTHON main.py --confirm-copy --show-entropy wifi -l "$len" --simple
            else
                $PYTHON main.py --confirm-copy --show-entropy wifi -l "$len"
            fi
            echo ""
            ;;
        10)
            clear
            echo ""
            echo "License Key Generator"
            echo "====================="
            echo ""
            $PYTHON main.py --confirm-copy --show-entropy license --segments 4 --segment-length 4
            echo ""
            ;;
        11)
            clear
            read -p "Number of recovery codes (6-12): " count
            read -p "Word-based codes? (y/n): " word_based
            if [[ "$word_based" == "y" || "$word_based" == "Y" ]]; then
                $PYTHON main.py --confirm-copy recovery -n "$count" --words
            else
                $PYTHON main.py --confirm-copy recovery -n "$count"
            fi
            echo ""
            ;;
        12)
            clear
            echo ""
            echo "OTP Secret (for 2FA apps)"
            echo "========================="
            echo ""
            $PYTHON main.py --confirm-copy --show-entropy otp
            echo ""
            ;;
        13)
            clear
            $PYTHON main.py --confirm-copy --interactive
            ;;
        14)
            clear
            read -p "Show last N entries (default 10): " num
            [[ -z "$num" ]] && num=10
            $PYTHON main.py --confirm-copy history --last "$num"
            echo ""
            pause
            ;;
        15)
            clear
            $PYTHON main.py --confirm-copy --help
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
            echo ""
            $PYTHON main.py --confirm-copy --preset strong --show-entropy
            echo ""
            ;;
        [Pp]2)
            clear
            echo ""
            echo "Preset: MEMORABLE (easy to say)"
            echo "================================="
            echo ""
            $PYTHON main.py --confirm-copy --preset memorable --show-entropy
            echo ""
            ;;
        [Pp]3)
            clear
            echo ""
            echo "Preset: DEVELOPER (40 char alphanumeric)"
            echo "========================================="
            echo ""
            $PYTHON main.py --confirm-copy --preset dev --show-entropy
            echo ""
            ;;
        [Pp]4)
            clear
            echo ""
            echo "Preset: WEB ACCOUNT (16 chars mixed)"
            echo "====================================="
            echo ""
            $PYTHON main.py --confirm-copy --preset web --show-entropy
            echo ""
            ;;
        [Pp]5)
            clear
            echo ""
            echo "Preset: WIFI KEY (20 chars)"
            echo "============================"
            echo ""
            $PYTHON main.py --confirm-copy --preset wifi --show-entropy
            echo ""
            ;;
        [Pp]6)
            clear
            echo ""
            echo "Preset: LICENSE KEY (5x5 format)"
            echo "================================="
            echo ""
            $PYTHON main.py --confirm-copy --preset key --show-entropy
            echo ""
            ;;
        *)
            echo "Invalid option. Press Enter to try again..."
            read
            ;;
    esac
done
