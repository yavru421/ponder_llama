import os
import json
import logging
import uuid
from pathlib import Path
from module_common import atomic_write, get_output_dir

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def generate_prompt(goal, negatives, tools, search_terms, context_folder):
    prompt = f"Goal: {goal}\nNegative Prompts: {negatives}\nTools: {tools}\nSearch Terms: {search_terms}\nContext Folder: {context_folder or '[default]'}\nPlease perform the task as described, using the tools and context provided."
    return prompt

def save_prompt(goal, negatives, tools, search_terms, context_folder):
    prompt = generate_prompt(goal, negatives, tools, search_terms, context_folder)
    prompt_id = str(uuid.uuid4())
    prompt_data = {
        "id": prompt_id,
        "goal": goal,
        "negatives": negatives,
        "tools": tools,
        "search_terms": search_terms,
        "context_folder": context_folder,
        "prompt": prompt
    }
    prompts_dir = "prompts"
    Path(prompts_dir).mkdir(parents=True, exist_ok=True)
    prompt_file = os.path.join(prompts_dir, f"prompt_{prompt_id}.json")
    with open(prompt_file, "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, indent=4, ensure_ascii=False)
    logging.info(f"Prompt form completed and saved as {prompt_file}")
    return prompt_file, prompt_id