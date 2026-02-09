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

# Create Release Package
echo "Step 2: Creating Release Package..."
VERSION="1.0.0"
RELEASE_NAME="passforge_v${VERSION}"
RELEASE_DIR="dist/${RELEASE_NAME}"
ARCHIVE="dist/${RELEASE_NAME}.tar.gz"

echo "Target Directory: $RELEASE_DIR"

rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

echo "Copying artifacts..."
cp dist/passforge "$RELEASE_DIR/"
cp README.md "$RELEASE_DIR/"
cp LICENSE "$RELEASE_DIR/"
cp passforge.example.json "$RELEASE_DIR/"
cp passforge_quick.sh "$RELEASE_DIR/"

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to copy files to release directory."
    exit 1
fi

echo ""
echo "Step 3: Packaging as tar.gz..."
tar -czf "$ARCHIVE" -C dist "$RELEASE_NAME"

if [ $? -ne 0 ]; then
    echo "[ERROR] Compression failed."
    exit 1
fi

echo ""
echo "============================================"
echo "  Build and Packaging Successful!"
echo "============================================"
echo ""
echo "Binary:   dist/passforge"
echo "Folder:   $RELEASE_DIR/"
echo "Archive: $ARCHIVE"
echo ""

# Test the executable
echo "Testing the binary..."
./dist/passforge --version
./dist/passforge random -l 12

echo ""
echo "Process complete!"


