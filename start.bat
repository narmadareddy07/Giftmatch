
@echo off
title GiftMatch - Launcher
cd /d "%~dp0"

echo ====================================
echo        Starting GiftMatch
echo ====================================
echo.

if not exist "app.py" (
    echo ERROR: app.py was not found in this folder.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt was not found.
    pause
    exit /b 1
)

echo Installing required packages...
py -3 -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed.
    pause
    exit /b 1
)

echo.
echo Launching GiftMatch...
py -3 app.py

if errorlevel 1 (
    echo.
    echo GiftMatch stopped because of an error.
    pause
)
