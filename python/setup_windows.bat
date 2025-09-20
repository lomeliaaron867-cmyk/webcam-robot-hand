@echo off
setlocal

echo ==========================================
echo Webcam Robotic Hand - Windows Setup
echo ==========================================
echo.

cd /d "%~dp0"

py -3.11 --version >nul 2>nul
if errorlevel 1 (
    echo Python 3.11 was not found.
    echo Install Python 3.11 and run this file again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3.11 -m venv .venv

    if errorlevel 1 (
        echo Failed to create the virtual environment.
        pause
        exit /b 1
    )
)

echo Installing dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Setup failed.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully.
echo Run run_windows.bat to start the program.
pause