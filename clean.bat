@echo off
echo 🧹 Cleaning ResearchForge
echo ========================

echo Removing output files...
if exist "output\*.json" del /q "output\*.json"
if exist "output\*.md" del /q "output\*.md"
if exist "output\*.txt" del /q "output\*.txt"

echo Removing prompt cache...
if exist "prompts\*.json" del /q "prompts\*.json"

echo Removing Python cache...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "tests\__pycache__" rmdir /s /q "tests\__pycache__"

echo Removing temporary files...
if exist "temp_*.txt" del /q "temp_*.txt"

echo ✅ Cleanup complete!
pause