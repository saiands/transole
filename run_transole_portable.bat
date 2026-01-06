@echo off
SETLOCAL
TITLE Transol VMS - Portable Launcher

echo =====================================================
echo      Transol VMS - Portable Startup Script
echo =====================================================
echo.

REM 1. Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not found in your PATH.
    echo Please install Python 3.9 or higher from python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    EXIT /B
)

REM 2. Setup Virtual Environment
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating 'venv'...
    python -m venv venv
    if not exist "venv" (
        echo [ERROR] Failed to create virtual environment. 
        pause
        EXIT /B
    )
    echo [INFO] Virtual environment created successfully.
    
    echo [INFO] Installing dependencies from requirements.txt...
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [INFO] Virtual environment found. Activating...
    call venv\Scripts\activate
)

REM 3. Database migrations
echo.
echo [INFO] Applying database migrations...
python manage.py migrate

REM 4. Start Server
echo.
echo [INFO] Starting Django Server...
echo [INFO] Opening browser...
timeout /t 3 >nul
start "" "http://127.0.0.1:8000/"

echo.
echo =====================================================
echo Server is running. Close this window to stop the app.
echo =====================================================
python manage.py runserver

pause
