@echo off
TITLE Stop Transol VMS
echo =====================================================
echo      Stop Transol VMS
echo =====================================================
echo.
echo Searching for Transol VMS (Port 8000)...

set FOUND=0
FOR /F "tokens=5" %%P IN ('netstat -a -n -o ^| findstr ":8000" ^| findstr /i "LISTENING"') DO (
    echo Found running process (PID: %%P). Killing...
    taskkill /F /PID %%P
    set FOUND=1
)

IF %FOUND%==0 (
    echo No server instance found running on port 8000.
) ELSE (
    echo.
    echo Server has been stopped successfully.
)

echo.
pause
