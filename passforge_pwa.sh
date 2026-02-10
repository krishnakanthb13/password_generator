#!/bin/bash

# PassForge PWA Launcher for Linux/macOS
# This script starts the local FastAPI server and opens the browser.

echo -e "\n +=========================================+"
echo -e " |         PassForge Web Interface         |"
echo -e " +=========================================+\n"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERR] Python3 is not installed."
    exit 1
fi

# Kill any existing process on port 8093
echo "[1/4] Checking for existing PWA processes..."
if command -v fuser &> /dev/null; then
    fuser -k 8093/tcp &> /dev/null
elif command -v lsof &> /dev/null; then
    lsof -ti:8093 | xargs kill -9 &> /dev/null
fi

# Check for dependencies
echo "[2/4] Verifying dependencies..."
if ! python3 -c "import fastapi, uvicorn" &> /dev/null; then
    echo "[!] Missing PWA dependencies. Installing..."
    pip3 install fastapi uvicorn python-multipart
fi

# Start the server in the background
echo "[3/4] Starting PassForge Web Server..."
uvicorn pwa.server:app --host 127.0.0.1 --port 8093 --log-level warning &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Open browser (cross-platform)
echo "[3/3] Opening browser at http://127.0.0.1:8093"
if command -v xdg-open &> /dev/null; then
    xdg-open "http://127.0.0.1:8093"
elif command -v open &> /dev/null; then
    open "http://127.0.0.1:8093"
else
    echo "[!] Could not detect browser opener. Please visit http://127.0.0.1:8093 manually."
fi

echo -e "\n[OK] PWA is running! (PID: $SERVER_PID)"
echo "Keep this terminal open while using the web interface."
echo "Press Ctrl+C to stop the server when finished."

# Trap Ctrl+C to kill the background process
trap "kill $SERVER_PID; echo -e '\nServer stopped.'; exit" SIGINT

# Wait for background process
wait $SERVER_PID
