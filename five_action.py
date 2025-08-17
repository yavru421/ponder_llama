"""
five_action.py (StepForge Action Plan - Smart Assistant)

This script analyzes the latest pipeline output, queries multiple Llama models for review and improvement, compares outputs, flags off-topic code, and attempts to auto-generate a scaffold for the user's goal. It produces a comprehensive Action_plan.md with actionable warnings, suggestions, and all previous analysis.
"""

import os
import re
import glob
import json
import tempfile
import subprocess
from datetime import datetime
from typing import Optional

try:
    from llama_api_client import LlamaAPIClient
except ImportError:
    LlamaAPIClient = None

def extract_python_code_blocks(md_text):
    return re.findall(r'```python\s*([\s\S]*?)```', md_text, re.MULTILINE)

def extract_section(md_text, section_title):
    pattern = rf"^#+\s*{re.escape(section_title)}[\r\n]+([\s\S]+?)(?=^#+|\Z)"
    match = re.search(pattern, md_text, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else None

def summarize_markdown(md_text):
    summary = {}
    for section in ["Overview", "Explanation", "Methodology", "Instructions", "Summary"]:
        content = extract_section(md_text, section)
        if content:
            summary[section] = content
    code_blocks = extract_python_code_blocks(md_text)
    summary["code_blocks"] = code_blocks
    guess = None
    if "Overview" in summary:
        guess = summary["Overview"].split(". ")[0].strip()
    elif code_blocks:
        code = code_blocks[0]
        # Heuristic: try to guess topic from code
        if "quantum" in code.lower():
            guess = "Research and demonstrate quantum computing concepts."
        elif "calculator" in code.lower():
            guess = "Build a calculator that adds and multiplies numbers."
        elif "todo" in code.lower():
            guess = "Implement a todo/task manager app."
        else:
            guess = "Implement the main logic shown in the code block."
    summary["prompt_guess"] = guess
    return summary

def call_llama_review(prompt: str, code: str, model: str) -> Optional[str]:
    if not LlamaAPIClient:
        return None
    try:
        client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
        messages = [
            {"role": "system", "content": f"You are a senior Python developer and reviewer. The user prompt is: {prompt}"},
            {"role": "user", "content": f"Here is the code block to review and improve.\n\n```python\n{code}\n```\n\nPlease provide:\n- A short summary of what this code does.\n- Is it relevant to the prompt?\n- Suggestions for improvement or a better implementation.\n- If the code is off-topic, suggest a scaffold for the user's goal."}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return getattr(response.completion_message.content, 'text', None)
    except Exception as e:
        return f"[Llama API error: {e}]"

def extract_imports(code):
    imports = set()
    for line in code.splitlines():
        line = line.strip()
        if line.startswith('import '):
            parts = line.split()
            if len(parts) > 1:
                imports.add(parts[1].split('.')[0])
        elif line.startswith('from '):
            parts = line.split()
            if len(parts) > 1:
                imports.add(parts[1].split('.')[0])
    return sorted(imports)

def check_dependencies(imports):
    import importlib.util
    missing = []
    for pkg in imports:
        if pkg in ('sys', 'os', 're', 'math', 'json', 'datetime', 'random', 'time', 'glob', 'tempfile', 'subprocess', 'typing'):
            continue
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    return missing

def lint_code(code):
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as tf:
        tf.write(code)
        temp_path = tf.name
    try:
        result = subprocess.run(['flake8', temp_path], capture_output=True, text=True, timeout=10)
        lint_output = result.stdout.strip() or 'No linting issues found.'
        # Suggest fixes for common issues
        fix_suggestions = []
        if 'E302' in lint_output:
            fix_suggestions.append('Add 2 blank lines before function or class definitions.')
        if 'E305' in lint_output:
            fix_suggestions.append('Add 2 blank lines after class or function definitions.')
        if fix_suggestions:
            lint_output += '\n\nFix Suggestions:\n- ' + '\n- '.join(fix_suggestions)
    except Exception as e:
        lint_output = f'Linting failed: {e}'
    finally:
        os.unlink(temp_path)
    return lint_output

def run_code(code):
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as tf:
        tf.write(code)
        temp_path = tf.name
    try:
        result = subprocess.run(['python', temp_path], capture_output=True, text=True, timeout=10)
        output = result.stdout.strip()
        error = result.stderr.strip()
        if result.returncode == 0:
            run_result = f'Output:\n{output or "(No output)"}'
        else:
            run_result = f'Error:\n{error or "Unknown error"}\n\nTraceback:\n{error}'
    except Exception as e:
        run_result = f'Execution failed: {e}'
    finally:
        os.unlink(temp_path)
    return run_result

def suggest_resources(prompt_or_code):
    suggestions = []
    text = prompt_or_code.lower()
    if 'quantum' in text:
        suggestions.append('[Qiskit Textbook](https://qiskit.org/textbook/) - Interactive introduction to quantum computing.')
        suggestions.append('[IBM Quantum Documentation](https://quantum-computing.ibm.com/docs/) - Official IBM Qiskit and quantum hardware docs.')
    if 'numpy' in text:
        suggestions.append('[NumPy Documentation](https://numpy.org/doc/) - Reference for numerical computing in Python.')
    if 'python' in text:
        suggestions.append('[Python Official Docs](https://docs.python.org/3/) - The official Python language documentation.')
    if 'todo' in text or 'task' in text:
        suggestions.append('[Flask Documentation](https://flask.palletsprojects.com/) - Lightweight Python web framework.')
        suggestions.append('[FastAPI Documentation](https://fastapi.tiangolo.com/) - Modern, fast web framework for APIs.')
    if not suggestions:
        suggestions.append('No specific resources found. Try searching for tutorials or documentation related to your topic.')
    return suggestions

def find_latest_prompt_file():
    prompt_dir = 'prompts'
    prompt_files = sorted(glob.glob(os.path.join(prompt_dir, 'prompt_*.json')), key=os.path.getmtime, reverse=True)
    return prompt_files[0] if prompt_files else None

def extract_prompt_params(prompt_file):
    if not prompt_file or not os.path.exists(prompt_file):
        return {}
    with open(prompt_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {
        'goal': data.get('goal'),
        'negatives': data.get('negatives'),
        'tools': data.get('tools'),
        'search_terms': data.get('search_terms'),
        'context_folder': data.get('context_folder'),
        'prompt': data.get('prompt')
    }

def write_action_plan(summary, params, lint_output, run_result, imports, missing, resources, output_md_path, review_maverick, review_scout, scaffold_suggestion, code_relevance_flag, warning):
    pip_suggestion = f"pip install {' '.join(missing)}" if missing else None
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(f"# StepForge Action Plan\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"---\n\n")

        # User Goal
        f.write("## User Goal\n\n")
        if summary.get("prompt_guess"):
            f.write(f"{summary['prompt_guess']}\n\n")
        else:
            f.write("_Could not determine the original user goal._\n\n")
        f.write(f"---\n\n")

        # Parameter Traceback
        f.write("## Parameter Traceback\n\n")
        for k, v in params.items():
            f.write(f"**{k.replace('_', ' ').title()}:** {v if v else '_Not provided_'}\n\n")
        f.write(f"---\n\n")

        # Pipeline Output Summary
        f.write("## Pipeline Output Summary\n\n")
        if summary.get("Overview"):
            f.write(f"{summary['Overview']}\n\n")
        else:
            f.write("_No overview section found in the output._\n\n")
        f.write(f"---\n\n")

        # Main Steps Taken
        f.write("## Main Steps Taken\n\n")
        f.write("1. User provided a prompt and parameters.\n")
        f.write("2. The pipeline generated a markdown summary and code block(s) based on the prompt.\n")
        f.write("3. This script analyzed the output, reviewed the code, and generated this action plan.\n\n")
        f.write(f"---\n\n")

        # Code Quality & Linting
        f.write("## Code Quality & Linting\n\n")
        f.write(f"{lint_output}\n\n")
        f.write(f"---\n\n")

        # Automated Test/Run Results
        f.write("## Automated Test/Run Results\n\n")
        f.write(f"{run_result}\n\n")
        f.write(f"---\n\n")

        # Dependency Analysis
        f.write("## Dependency Analysis\n\n")
        f.write(f"**Imports found:** {', '.join(imports) if imports else 'None'}\n\n")
        if missing:
            f.write(f"**Missing packages:** {', '.join(missing)}\n\n")
            if pip_suggestion:
                f.write(f"**To install missing packages:** `{pip_suggestion}`\n\n")
        else:
            f.write("All required packages are installed.\n\n")
        f.write(f"---\n\n")

        # Llama Model Reviews
        f.write("## Llama Model Reviews\n\n")
        f.write("### Llama-4-Maverick-17B-128E-Instruct-FP8\n\n")
        f.write(f"{review_maverick}\n\n")
        f.write("### Llama-4-Scout-17B-16E-Instruct-FP8\n\n")
        f.write(f"{review_scout}\n\n")
        f.write(f"---\n\n")

        # Code Relevance & Scaffold
        f.write("## Code Relevance & Scaffold\n\n")
        if code_relevance_flag:
            f.write(f"**Warning:** {warning}\n\n")
        if scaffold_suggestion:
            f.write(f"### Suggested Scaffold or Improvement\n{scaffold_suggestion}\n\n")
        f.write(f"---\n\n")

        # Actionable Next Steps
        f.write("## Actionable Next Steps\n\n")
        f.write("- Review the summary, code, and model suggestions below.\n")
        f.write("- Consider running or adapting the code for your needs.\n")
        f.write("- Use the pivots section for inspiration on how to extend or redirect your project.\n\n")
        f.write(f"---\n\n")

        # Alternative Directions / Pivots
        f.write("## Alternative Directions / Pivots\n\n")
        f.write("1. **Deeper Exploration:** Focus on advanced or niche aspects of the topic.\n")
        f.write("2. **Practical Application:** Apply the output to a real-world scenario or dataset.\n")
        f.write("3. **Comparative Study:** Compare this approach with alternatives or related fields.\n\n")
        f.write(f"---\n\n")

        # Resource Enrichment
        f.write("## Resource Enrichment\n\n")
        for r in resources:
            f.write(f"- {r}\n")
        f.write(f"\n---\n\n")

        # Feedback Section
        f.write("## Feedback\n\n")
        f.write("_Please provide your feedback, comments, or suggestions below:_\n\n")
        f.write("> [ ] Satisfied\n> [ ] Needs improvement\n> [ ] Other: ___________________________\n\n")
        f.write(f"---\n\n")

        # Appendix: Main Code Block(s)
        f.write("## Appendix: Main Code Block(s)\n\n")
        if summary.get("code_blocks") and len(summary["code_blocks"]):
            for i, code in enumerate(summary["code_blocks"], 1):
                f.write(f"### Code Block {i}\n")
                f.write(f"```python\n{code.strip()}\n```\n\n")
        else:
            f.write("_No Python code blocks found in the output._\n\n")
        f.write(f"---\n\n")
        f.write("_Action plan generated by StepForge pipeline smart assistant._\n")

def main():
    output_dir = "output"

    # Find the latest prompt file and extract its id
    prompt_file = find_latest_prompt_file()
    if not prompt_file:
        print("No prompt files found in the prompts directory.")
        return

    with open(prompt_file, 'r', encoding='utf-8') as pf:
        prompt_data = json.load(pf)
    prompt_id = prompt_data.get('id')
    user_goal = prompt_data.get('goal', '')

    # Find the latest output markdown file matching the prompt id
    output_md_path = None
    if prompt_id:
        candidate = os.path.join(output_dir, f"output_{prompt_id}.md")
        if os.path.exists(candidate):
            output_md_path = candidate

    if not output_md_path:
        # Fallback: use the most recent output_*.md file
        md_files = sorted(glob.glob(os.path.join(output_dir, "output_*.md")), key=os.path.getmtime, reverse=True)
        if not md_files:
            print("No output markdown files found in the output directory.")
            return
        output_md_path = md_files[0]

    with open(output_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    summary = summarize_markdown(md_text)

    # Parameter Traceback
    params = extract_prompt_params(prompt_file)

    # Code Quality & Linting, Automated Test/Run, Dependency Analysis
    code = summary["code_blocks"][0] if summary.get("code_blocks") and len(summary["code_blocks"]) else ""
    lint_output = lint_code(code) if code else "No code to lint."
    run_result = run_code(code) if code else "No code to run."
    imports = extract_imports(code) if code else []
    missing = check_dependencies(imports) if imports else []

    # Resource Enrichment
    resources = suggest_resources(params.get('goal', '') + '\n' + code)

    # Query both Llama models for review and improvement
    review_maverick = call_llama_review(user_goal, code, "Llama-4-Maverick-17B-128E-Instruct-FP8") or "[No response from Maverick]"
    review_scout = call_llama_review(user_goal, code, "Llama-4-Scout-17B-16E-Instruct-FP8") or "[No response from Scout]"

    # Check if code is relevant to the prompt
    code_relevance_flag = False
    warning = ""
    scaffold_suggestion = ""

    if user_goal and code:
        if user_goal.lower() not in code.lower() and not any(word in code.lower() for word in user_goal.lower().split()):
            code_relevance_flag = True
            warning = "The code block does not appear to match your prompt."
            # Try to extract a scaffold suggestion from model reviews
            for review in (review_maverick, review_scout):
                if review and "scaffold" in review.lower():
                    scaffold_suggestion = review
                    break
    elif user_goal and not code:
        code_relevance_flag = True
        warning = "No code block was found for your prompt."
        # Try to get a scaffold from the models
        scaffold_suggestion = call_llama_review(user_goal, "", "Llama-4-Maverick-17B-128E-Instruct-FP8") or "[No scaffold generated]"

    # Write Action Plan
    action_plan_path = os.path.join(output_dir, "Action_plan.md")
    write_action_plan(summary, params, lint_output, run_result, imports, missing, resources, action_plan_path, review_maverick, review_scout, scaffold_suggestion, code_relevance_flag, warning)
    print(f"\n[StepForge] Action plan written to: {action_plan_path}")

if __name__ == "__main__":
    main()