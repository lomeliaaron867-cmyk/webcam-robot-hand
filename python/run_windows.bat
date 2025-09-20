@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo The Python environment has not been created.
    echo Run setup_windows.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" hand_controller.py

if errorlevel 1 (
    echo.
    echo The program stopped because of an error.
    pause
)