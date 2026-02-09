#!/bin/bash
# Quick launcher - generates a random password instantly

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "[ERROR] Python not found. Install from https://python.org"
    exit 1
fi

$PYTHON main.py --show-entropy random -l 16
