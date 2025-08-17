# This is the correct step-four prompt generator script, renamed from 4.py
from module4 import save_prompt
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    print("Welcome to the LLaMA Prompt Form. Please answer the following (press Enter to use default):")
    print("Tip: Providing a clear overview and summary in your goal will improve the final Action Plan report. Results will be analyzed for code quality, dependencies, and feedback.")
    goal = input("Goal/Task Description: ").strip()
    if not goal:
        goal = "Research and summarize the topic of quantum computing"
    negatives = input("Negative Prompts (what to avoid): ").strip()
    if not negatives:
        negatives = "No opinions, no unverified claims, no code, no print-only scripts"
    tools = input("Tools to utilize (comma-separated): ").strip()
    if not tools:
        tools = "Web search, academic papers, Wikipedia"
    search_terms = input("Words/phrases to search in context (comma-separated): ").strip()
    if not search_terms:
        search_terms = "quantum computing, qubits, superposition, entanglement"
    context_folder = input("Context folder for generated files (leave blank for default): ").strip()
    # context_folder can remain blank for default
    prompt_file, prompt_id = save_prompt(goal, negatives, tools, search_terms, context_folder)
    print(f"\nPrompt saved to: {prompt_file}\nPrompt ID: {prompt_id}")

if __name__ == "__main__":
    main()