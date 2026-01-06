#!/bin/bash
# MacOS/Linux Launcher for Transol VMS

echo "====================================================="
echo "     Transol VMS - Portable Startup Script"
echo "====================================================="
echo ""

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed. Please install it first."
    exit 1
fi

# 2. Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "[INFO] Virtual environment not found. Creating 'venv'..."
    python3 -m venv venv
    
    echo "[INFO] Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "[INFO] Virtual environment found. Activating..."
    source venv/bin/activate
fi

# 3. Database migrations
echo ""
echo "[INFO] Applying database migrations..."
python manage.py migrate

# 4. Start Server
echo ""
echo "[INFO] Starting Django Server..."
echo "[INFO] Opening browser in 3 seconds..."

# Function to run server and open browser
(sleep 3 && open "http://127.0.0.1:8000/") &
python manage.py runserver

