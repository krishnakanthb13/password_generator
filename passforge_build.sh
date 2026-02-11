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
    --name passforge_v1.2.0 \
    --console \
    --add-data "src:src" \
    --add-data "data:data" \
    --hidden-import colorama \
    --hidden-import json \
    --hidden-import secrets \
    --hidden-import base64 \
    --hidden-import math \
    --hidden-import uuid \
    --hidden-import cryptography \
    --hidden-import zxcvbn \
    --hidden-import qrcode \
    --hidden-import dotenv \
    --exclude-module yt_dlp \
    --exclude-module tensorflow \
    --exclude-module boto3 \
    --exclude-module botocore \
    --exclude-module google \
    --exclude-module grpc \
    --exclude-module shapely \
    --exclude-module orjson \
    --exclude-module websockets \
    --exclude-module mutagen \
    --exclude-module brotli \
    --exclude-module certifi \
    --exclude-module secretstorage \
    --exclude-module curl_cffi \
    --exclude-module baidubce \
    --exclude-module qianfan \
    --exclude-module fake_useragent \
    --exclude-module notebook \
    --exclude-module jupyter \
    --exclude-module IPython \
    --exclude-module pygments \
    --exclude-module zmq \
    --exclude-module pygame \
    --exclude-module numpy \
    --exclude-module matplotlib \
    --exclude-module pandas \
    --exclude-module scipy \
    --exclude-module pydantic \
    --exclude-module langchain \
    --exclude-module anyio \
    --exclude-module opentelemetry \
    --exclude-module pyarrow \
    --exclude-module dask \
    --exclude-module fsspec \
    --exclude-module jinja2 \
    --exclude-module regex \
    --exclude-module jsonschema \
    --exclude-module lark \
    --exclude-module nbformat \
    --exclude-module zoneinfo \
    --exclude-module tkinter \
    --exclude-module tcl \
    --exclude-module tk \
    --exclude-module qtpy \
    --exclude-module PyQt5 \
    --exclude-module PyQt6 \
    --exclude-module PySide2 \
    --exclude-module PySide6 \
    --exclude-module sklearn \
    --exclude-module scikit-learn \
    --exclude-module torch \
    --exclude-module torchvision \
    --exclude-module cv2 \
    --exclude-module sqlalchemy \
    --exclude-module flask \
    --exclude-module django \
    --exclude-module unittest \
    --exclude-module docutils \
    --exclude-module PIL.ImageQt \
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
VERSION="1.2.0"
RELEASE_NAME="passforge_v${VERSION}"
RELEASE_DIR="dist/${RELEASE_NAME}"
ARCHIVE="dist/${RELEASE_NAME}.tar.gz"

echo "Target Directory: $RELEASE_DIR"

rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

echo "Copying artifacts..."
cp dist/passforge_v1.2.0 "$RELEASE_DIR/"
cp README.md "$RELEASE_DIR/"
cp LICENSE "$RELEASE_DIR/"
cp passforge.example.json "$RELEASE_DIR/"
cp .example.env "$RELEASE_DIR/"
cp passforge_quick.sh "$RELEASE_DIR/"
cp passforge_launch.sh "$RELEASE_DIR/"
cp passforge_pwa.sh "$RELEASE_DIR/"
cp DESIGN_PHILOSOPHY.md "$RELEASE_DIR/"
cp CODE_DOCUMENTATION.md "$RELEASE_DIR/"
cp SECURITY.md "$RELEASE_DIR/"
cp RELEASE_NOTES.md "$RELEASE_DIR/"
cp -r data "$RELEASE_DIR/"
cp -r pwa "$RELEASE_DIR/"

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
echo "Binary:   dist/passforge_v1.2.0"
echo "Folder:   $RELEASE_DIR/"
echo "Archive:  dist/passforge_v1.2.0.tar.gz"
echo ""

# Test the executable
echo "Testing the binary..."
./dist/passforge_v1.2.0 --version
./dist/passforge_v1.2.0 random -l 12

echo ""
echo "Process complete!"
