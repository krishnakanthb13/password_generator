#!/bin/bash
# PassForge Build Script - Creates standalone executable using PyInstaller

echo "============================================"
echo "  PassForge Build Script"
echo "============================================"
echo ""

# Check if PyInstaller is installed
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

echo ""
echo "Building PassForge executable..."
echo ""

# Build the executable
pyinstaller --onefile \
    --name passforge \
    --console \
    --add-data "src:src" \
    --hidden-import colorama \
    --hidden-import json \
    --hidden-import secrets \
    --hidden-import base64 \
    --hidden-import math \
    --hidden-import uuid \
    main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Build FAILED!"
    exit 1
fi

echo ""
echo "============================================"
echo "  Build Complete!"
echo "============================================"
echo ""
echo "Executable location: dist/passforge"
echo ""

# Test the executable
echo "Testing the executable..."
./dist/passforge --version
./dist/passforge random -l 12

echo ""
echo "Build successful!"
