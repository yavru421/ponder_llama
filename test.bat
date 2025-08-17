@echo off
echo 🧪 Running ResearchForge Tests
echo =============================

echo Running Python tests...
python -m pytest tests/ -v

echo Running code quality checks...
echo Checking PEP8 compliance...
python -m flake8 *.py --max-line-length=88 --ignore=E203,W503

echo Running specific module tests...
python test_calculator.py
python test_quantum.py

echo ✅ All tests completed!
pause