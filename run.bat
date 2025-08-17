@echo off
echo 🚀 Starting ResearchForge GUI...
echo ============================

echo Checking dependencies...
python -c "import requests, json" 2>nul
if errorlevel 1 (
    echo ❌ Missing dependencies! Run setup.bat first
    pause
    exit /b 1
)

echo Starting GUI...
powershell -ExecutionPolicy Bypass -File "ponder_llama_gui.ps1"

echo 👋 GUI closed. Check output/ folder for results!
pause