# 🚀 Quick Start Guide

## Windows Users (Recommended)

### Option 1: Batch Files (Simplest)
```batch
# Setup
setup.bat

# Run GUI
run.bat

# Run tests
test.bat

# Clean up
clean.bat
```

### Option 2: PowerShell (Most Features)
```powershell
# Setup
.\tasks.ps1 setup

# Run GUI
.\tasks.ps1 gui

# Run StepForge pipeline
.\tasks.ps1 pipeline

# Run tests
.\tasks.ps1 test

# Get help
.\tasks.ps1 help
```

### Option 3: Python Task Runner (Cross-Platform)
```bash
# Setup
python tasks.py setup

# Run complete pipeline
python tasks.py pipeline

# Run tests
python tasks.py test

# Install dev tools
python tasks.py dev-install
```

### Option 4: NPM Scripts (If you have Node.js)
```bash
# Setup
npm run setup

# Run GUI
npm run gui

# Run pipeline
npm run pipeline

# Format code
npm run format
```

## Linux/Mac Users

Use the Python task runner:
```bash
python tasks.py setup
python tasks.py pipeline
python tasks.py test
```

## Development Workflow

1. **First time setup:**
   ```batch
   setup.bat
   ```

2. **Daily usage:**
   ```batch
   run.bat
   ```

3. **Development:**
   ```powershell
   .\tasks.ps1 dev
   .\tasks.ps1 test
   ```

4. **Before committing:**
   ```bash
   npm run format
   npm run lint
   ```

## What Each Task Does

- **setup**: Installs dependencies, creates directories
- **gui**: Launches the Windows GUI interface
- **pipeline**: Runs the complete StepForge workflow
- **test**: Runs all tests and quality checks
- **clean**: Removes generated files and caches
- **dev**: Installs additional development tools