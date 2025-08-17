#!/usr/bin/env python3
"""
StepForge Task Runner - Step 6: Automation
==========================================
Windows-friendly task automation following StepForge methodology.
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

class TaskRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent

    def run_command(self, command, description):
        """Execute a command with error handling."""
        print(f"🔄 {description}")
        print(f"   Running: {command}")

        try:
            result = subprocess.run(command, shell=True, check=True,
                                  capture_output=True, text=True)
            print(f"✅ {description} - Success")
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} - Failed")
            print(f"Error: {e.stderr}")
            return False

    def setup(self):
        """Install dependencies and setup project."""
        tasks = [
            ("pip install -r requirements.txt", "Installing dependencies"),
            ("pip install -r requirements-dev.txt", "Installing dev dependencies"),
        ]

        # Create directories
        for dir_name in ["output", "prompts", "context"]:
            os.makedirs(dir_name, exist_ok=True)

        for command, description in tasks:
            if not self.run_command(command, description):
                return False

        print("🎉 Setup completed successfully!")
        return True

    def test(self):
        """Run all tests."""
        tasks = [
            ("python -m pytest tests/ -v", "Running pytest"),
            ("python -m flake8 *.py --max-line-length=88", "Code quality check"),
            ("python test_calculator.py", "Calculator tests"),
            ("python test_quantum.py", "Quantum tests"),
        ]

        for command, description in tasks:
            self.run_command(command, description)

    def clean(self):
        """Clean generated files."""
        patterns = [
            "output/*.json", "output/*.md", "output/*.txt",
            "prompts/*.json", "temp_*.txt"
        ]

        for pattern in patterns:
            try:
                for file in Path(".").glob(pattern):
                    file.unlink()
                    print(f"🗑️  Removed {file}")
            except Exception as e:
                print(f"⚠️  Could not remove {pattern}: {e}")

        # Remove __pycache__ directories
        for pycache in Path(".").rglob("__pycache__"):
            try:
                import shutil
                shutil.rmtree(pycache)
                print(f"🗑️  Removed {pycache}")
            except Exception as e:
                print(f"⚠️  Could not remove {pycache}: {e}")

    def stepforge_pipeline(self):
        """Run the complete StepForge pipeline."""
        print("🔬 Starting StepForge Pipeline")
        print("==============================")

        steps = [
            ("python four_promptgen.py", "Step 4: Prompt Generation"),
            ("python 3.py", "Step 3: AI Processing"),
            ("python five_action.py", "Step 5: Action Planning"),
        ]

        for command, description in steps:
            if not self.run_command(command, description):
                print(f"❌ Pipeline failed at: {description}")
                return False

        print("🎉 StepForge Pipeline completed successfully!")
        return True

    def dev_install(self):
        """Install additional development tools."""
        dev_tools = [
            ("pip install black", "Code formatter"),
            ("pip install isort", "Import sorter"),
            ("pip install mypy", "Type checker"),
            ("pip install pre-commit", "Pre-commit hooks"),
        ]

        for command, description in dev_tools:
            self.run_command(command, description)

def main():
    parser = argparse.ArgumentParser(description="ResearchForge Task Runner")
    parser.add_argument("task", choices=[
        "setup", "test", "clean", "pipeline", "dev-install"
    ], help="Task to run")

    args = parser.parse_args()
    runner = TaskRunner()

    if args.task == "setup":
        runner.setup()
    elif args.task == "test":
        runner.test()
    elif args.task == "clean":
        runner.clean()
    elif args.task == "pipeline":
        runner.stepforge_pipeline()
    elif args.task == "dev-install":
        runner.dev_install()

if __name__ == "__main__":
    main()