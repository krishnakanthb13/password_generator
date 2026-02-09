#!/bin/bash
# ============================================
#   PassForge - Password Generator CLI
#   Unix/Linux/macOS Launcher
# ============================================

# Trap signals for graceful shutdown
trap 'echo " Interrupted. Exiting..."; exit 0' SIGINT SIGTERM

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    echo -e "${BLUE}========================================"
    echo "  PASSFORGE - Password Generator CLI"
    echo -e "========================================${NC}"
    echo ""
    echo "  Quick Generate:"
    echo "   [1] Random Password (16 chars)"
    echo "   [2] Random Password (custom length)"
    echo "   [3] Passphrase (4 words)"
    echo "   [4] Passphrase (custom)"
    echo "   [5] Leetspeak Password"
    echo "   [6] PIN Code"
    echo ""
    echo "  Advanced:"
    echo "   [7] JWT Secret"
    echo "   [8] UUID Token"
    echo "   [9] WiFi Key"
    echo "   [10] License Key"
    echo "   [11] Recovery Codes"
    echo "   [12] OTP Secret"
    echo ""
    echo "  Preset Profiles (One-Click):"
    echo "   [P1] Strong (32 chars, max security)"
    echo "   [P2] Memorable (easy to say)"
    echo "   [P3] Developer (40 char alphanumeric)"
    echo "   [P4] Web Account (16 chars)"
    echo "   [P5] WiFi Key (20 chars)"
    echo "   [P6] License Key (5x5 format)"
    echo ""
    echo "  Tools:"
    echo "   [13] Interactive Mode"
    echo "   [14] View History"
    echo "   [15] Show Help"
    echo ""
    echo "   [0] Exit"
    echo ""
}

pause() {
    read -p "Press Enter to continue..."
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
            $PYTHON main.py --show-entropy random -l 16
            echo ""
            pause
            ;;
        2)
            clear
            read -p "Enter password length (8-128): " len
            read -p "Show entropy analysis? (y/n): " show_ent
            if [[ "$show_ent" == "y" || "$show_ent" == "Y" ]]; then
                $PYTHON main.py --show-entropy random -l "$len"
            else
                $PYTHON main.py random -l "$len"
            fi
            echo ""
            pause
            ;;
        3)
            clear
            echo ""
            echo "Passphrase (4 words)"
            echo "===================="
            echo ""
            $PYTHON main.py --show-entropy phrase -w 4
            echo ""
            pause
            ;;
        4)
            clear
            read -p "Number of words (3-8): " words
            read -p "Separator (default -): " sep
            read -p "Capitalize words? (y/n): " cap
            [[ -z "$sep" ]] && sep="-"
            if [[ "$cap" == "y" || "$cap" == "Y" ]]; then
                $PYTHON main.py --show-entropy phrase -w "$words" -s "$sep" --capitalize
            else
                $PYTHON main.py --show-entropy phrase -w "$words" -s "$sep"
            fi
            echo ""
            pause
            ;;
        5)
            clear
            read -p "Number of words (2-5): " words
            $PYTHON main.py --show-entropy leet -w "$words"
            echo ""
            pause
            ;;
        6)
            clear
            read -p "PIN length (4-8): " len
            $PYTHON main.py --show-entropy pin -l "$len"
            echo ""
            pause
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
            $PYTHON main.py --show-entropy jwt --bits "$bits"
            echo ""
            pause
            ;;
        8)
            clear
            echo ""
            echo "UUID v4 Token"
            echo "============="
            echo ""
            $PYTHON main.py --show-entropy uuid
            echo ""
            pause
            ;;
        9)
            clear
            read -p "WiFi key length (8-63): " len
            read -p "Simple mode (alphanumeric only)? (y/n): " simple
            if [[ "$simple" == "y" || "$simple" == "Y" ]]; then
                $PYTHON main.py --show-entropy wifi -l "$len" --simple
            else
                $PYTHON main.py --show-entropy wifi -l "$len"
            fi
            echo ""
            pause
            ;;
        10)
            clear
            echo ""
            echo "License Key Generator"
            echo "====================="
            echo ""
            $PYTHON main.py --show-entropy license --segments 4 --segment-length 4
            echo ""
            pause
            ;;
        11)
            clear
            read -p "Number of recovery codes (6-12): " count
            read -p "Word-based codes? (y/n): " word_based
            if [[ "$word_based" == "y" || "$word_based" == "Y" ]]; then
                $PYTHON main.py recovery -n "$count" --words
            else
                $PYTHON main.py recovery -n "$count"
            fi
            echo ""
            pause
            ;;
        12)
            clear
            echo ""
            echo "OTP Secret (for 2FA apps)"
            echo "========================="
            echo ""
            $PYTHON main.py --show-entropy otp
            echo ""
            pause
            ;;
        13)
            clear
            $PYTHON main.py --interactive
            ;;
        14)
            clear
            read -p "Show last N entries (default 10): " num
            [[ -z "$num" ]] && num=10
            $PYTHON main.py history --last "$num"
            echo ""
            pause
            ;;
        15)
            clear
            $PYTHON main.py --help
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
            $PYTHON main.py --preset strong --show-entropy
            echo ""
            pause
            ;;
        [Pp]2)
            clear
            echo ""
            echo "Preset: MEMORABLE (easy to say)"
            echo "================================="
            echo ""
            $PYTHON main.py --preset memorable --show-entropy
            echo ""
            pause
            ;;
        [Pp]3)
            clear
            echo ""
            echo "Preset: DEVELOPER (40 char alphanumeric)"
            echo "========================================="
            echo ""
            $PYTHON main.py --preset dev --show-entropy
            echo ""
            pause
            ;;
        [Pp]4)
            clear
            echo ""
            echo "Preset: WEB ACCOUNT (16 chars mixed)"
            echo "====================================="
            echo ""
            $PYTHON main.py --preset web --show-entropy
            echo ""
            pause
            ;;
        [Pp]5)
            clear
            echo ""
            echo "Preset: WIFI KEY (20 chars)"
            echo "============================"
            echo ""
            $PYTHON main.py --preset wifi --show-entropy
            echo ""
            pause
            ;;
        [Pp]6)
            clear
            echo ""
            echo "Preset: LICENSE KEY (5x5 format)"
            echo "================================="
            echo ""
            $PYTHON main.py --preset key --show-entropy
            echo ""
            pause
            ;;
        *)
            echo "Invalid option. Press Enter to try again..."
            read
            ;;
    esac
done
