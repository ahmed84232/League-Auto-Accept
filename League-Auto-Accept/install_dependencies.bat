@echo off
title Python Dependencies Installer
echo ================================
echo   Installing Python Packages
echo ================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is NOT installed or not added to PATH.
    echo 👉 Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

:: Upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies...
echo.

python -m pip install ^
    PySide6>=6.6.0 ^
    aiohttp>=3.9.0 ^
    psutil>=5.9.0 ^
    qasync>=0.27.0

if errorlevel 1 (
    echo.
    echo ❌ Dependency installation failed
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies installed successfully!
echo.
pause
