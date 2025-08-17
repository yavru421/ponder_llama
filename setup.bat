@echo off
echo 🔬 ResearchForge Setup
echo ==================

echo Installing Python dependencies...
pip install -r requirements.txt

echo Installing development dependencies...
pip install -r requirements-dev.txt

echo Creating output directories...
if not exist "output" mkdir output
if not exist "prompts" mkdir prompts
if not exist "context" mkdir context

echo ✅ Setup complete! Run 'run.bat' to start the GUI
pause