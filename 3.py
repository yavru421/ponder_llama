import os
import json
import logging
import tempfile
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from llama_api_client import LlamaAPIClient
import requests
import glob
def atomic_write(file_path, data, mode='w', encoding='utf-8'):
    """Write data to a temp file and atomically move to destination."""
    dir_name = os.path.dirname(file_path)
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode=mode, encoding=encoding, dir=dir_name, delete=False) as tf:
        tf.write(data)
        tempname = tf.name
    shutil.move(tempname, file_path)

def get_output_dir() -> str:
    """Get output directory from env or default to 'output'."""
    return os.environ.get("PONDER_LLAMA_OUTPUT_DIR", "output")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

from typing import Tuple


# Helper to convert conversation history to the expected message format for LlamaAPIClient
def to_message_params(history: List[Dict[str, str]]) -> list:
    # If the API expects a specific MessageParam type, adapt here. For now, assume dicts are fine.
    # If not, you may need to import MessageParam and construct objects.
    return history

# Move advanced_conversation_flow above main to ensure it's defined before use
def advanced_conversation_flow(prompt: str, conversation_history: List[Dict[str, str]], max_turns: int = 5) -> List[Dict[str, str]]:
    output_dir = get_output_dir()
    # Allow user to set max_turns via env, min 5, max 10
    env_max_turns = os.environ.get("PONDER_LLAMA_MAX_TURNS")
    if env_max_turns:
        try:
            max_turns = int(env_max_turns)
            if max_turns < 5:
                max_turns = 5
            elif max_turns > 10:
                max_turns = 10
        except Exception:
            max_turns = 5
    # Ensure prompt is always defined
    if not prompt and conversation_history:
        prompt = conversation_history[-1]['content']
    if not prompt:
        prompt = ""
    for turn in range(max_turns):
        try:
            response, updated_history = get_llama_response(prompt, conversation_history)
            if not response:
                logging.warning("No response from LLaMA API. Stopping conversation.")
                break
            model_reply = getattr(response.completion_message.content, 'text', None)
            if not model_reply:
                logging.warning("No text in model response. Stopping conversation.")
                break
            logging.info(f"Turn {turn+1} - Model: {model_reply}")
            conversation_history.append({"role": "assistant", "content": model_reply})
            save_conversation(conversation_history, output_dir=output_dir)
            # Check for DDGS trigger
            if "use_ddgs:" in model_reply:
                query = model_reply.split("use_ddgs:", 1)[1].strip().split("\n")[0]
                ddgs_results = ddgs_search(query)
                user_msg = f"Here are the results of the DDGS search for '{query}': {json.dumps(ddgs_results, ensure_ascii=False)[:1000]}"
                conversation_history.append({"role": "user", "content": user_msg})
                prompt = user_msg
                continue
            # Optionally, ask the model for the next best question
            if turn < max_turns - 1:
                next_prompt = generate_next_prompt(conversation_history)
                if next_prompt:
                    logging.info(f"Next Prompt Suggestion: {next_prompt}")
                    prompt = next_prompt
                    conversation_history.append({"role": "user", "content": next_prompt})
                else:
                    logging.info("No next prompt generated. Ending conversation.")
                    break
        except Exception as e:
            logging.error(f"Error in conversation flow at turn {turn+1}: {e}")
            break
    return conversation_history

def get_llama_response(
    prompt: str,
    conversation_history: List[Dict[str, str]],
    model: str = "Llama-4-Maverick-17B-128E-Instruct-FP8"
) -> Tuple[Optional[Any], List[Dict[str, str]]]:
    """Send a prompt to the LLaMA API and return the response and updated conversation history."""
    try:
        client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
        messages = to_message_params(conversation_history + [{"role": "user", "content": prompt}])
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response, messages
    except Exception as e:
        logging.error(f"Error getting LLaMA response: {e}")
        return None, conversation_history

def ddgs_search(query: str) -> Dict:
    """Perform a DuckDuckGo search and return the results as a dict."""
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"DDGS search failed: {e}")
        return {"error": str(e)}

def generate_next_prompt(conversation_history: List[Dict[str, str]]) -> Optional[str]:
    """Ask the model to suggest a good next question based on the conversation so far."""
    prompt = "Based on our conversation so far, what would be a good next question to ask?"
    response, _ = get_llama_response(prompt, conversation_history)
    if response:
        return getattr(response.completion_message.content, 'text', None)
    return None

def save_conversation(conversation_history: List[Dict[str, str]], filename: str = "conversation_history.json", output_dir: str = "output"):
    try:
        output_dir = get_output_dir()
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        data = json.dumps(conversation_history, indent=4, ensure_ascii=False)
        atomic_write(file_path, data)
        logging.info(f"Conversation history saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save conversation history: {e}")

def save_summary(conversation_history: List[Dict[str, str]], filename: str = "output.json"):
    output_dir = get_output_dir()
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        summary = conversation_history[-1]["content"] if conversation_history else ""
        output = {
            "conversation_history": conversation_history,
            "summary": summary
        }
        file_path = os.path.join(output_dir, filename)
        data = json.dumps(output, indent=4, ensure_ascii=False)
        atomic_write(file_path, data)
        logging.info(f"Summary saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save summary: {e}")

def generate_markdown_summary(conversation_history: List[Dict[str, str]], output_json_path: str = "output.json", output_md_path: str = "output.md"):
    """Call LLaMA API to process the output.json and conversation, and write a narrative markdown file."""
    output_dir = get_output_dir()
    max_turns = 5  # Default value
    env_max_turns = os.environ.get("PONDER_LLAMA_MAX_TURNS")
    if env_max_turns:
        try:
            max_turns = int(env_max_turns)
            if max_turns < 5:
                max_turns = 5
            elif max_turns > 10:
                max_turns = 10
        except Exception:
            max_turns = 5
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_json_full = os.path.join(output_dir, output_json_path)
        with open(output_json_full, "r", encoding="utf-8") as f:
            output_data = json.load(f)
        prompt = (
            "Given the following conversation history and summary, generate a markdown file that narrates the conversation "
            "in a clear, engaging, and common-sense way, suitable for a project report or documentation. "
            "Focus on clarity, insight, and a helpful tone.\n\n"
            "Include an explicit ## Overview section at the top and a ## Summary section at the end. "
            "At the end of the markdown, include a complete, useful, and runnable Python script that implements the main logic discussed in the conversation. "
            "The script should be more than just a print statement or placeholder. "
            "For example, if the conversation is about a calculator, output a script that implements a Calculator class and a main function that demonstrates its use. "
            "Wrap the code in a Python code block.\n\n"
            f"Conversation History (JSON):\n{json.dumps(output_data['conversation_history'], ensure_ascii=False, indent=2)}\n\n"
            f"Summary: {output_data.get('summary', '')}\n\n"
            "---\n\nMarkdown Output:"
        )
        context_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        response, _ = get_llama_response(prompt, context_history)
        if response:
            markdown = getattr(response.completion_message.content, 'text', None)
            if markdown and markdown.strip():
                logging.info("Markdown summary generated. Results will be analyzed for code quality, dependencies, and feedback in the Action Plan.")
            else:
                logging.warning("No markdown text returned from LLaMA API or markdown is empty.")
        else:
            logging.warning("No response from LLaMA API for markdown summary.")
    except Exception as e:
        logging.error(f"Failed to generate markdown summary: {e}")
    # Ensure prompt is always defined
    prompt = conversation_history[-1]['content'] if conversation_history else ""
    for turn in range(max_turns):
        try:
            response, updated_history = get_llama_response(prompt, conversation_history)
            if not response:
                logging.warning("No response from LLaMA API. Stopping conversation.")
                break
            model_reply = getattr(response.completion_message.content, 'text', None)
            if not model_reply:
                logging.warning("No text in model response. Stopping conversation.")
                break
            logging.info(f"Turn {turn+1} - Model: {model_reply}")
            conversation_history.append({"role": "assistant", "content": model_reply})
            save_conversation(conversation_history, output_dir=output_dir)
            # Check for DDGS trigger
            if "use_ddgs:" in model_reply:
                query = model_reply.split("use_ddgs:", 1)[1].strip().split("\n")[0]
                ddgs_results = ddgs_search(query)
                user_msg = f"Here are the results of the DDGS search for '{query}': {json.dumps(ddgs_results, ensure_ascii=False)[:1000]}"
                conversation_history.append({"role": "user", "content": user_msg})
                prompt = user_msg
                continue
            # Optionally, ask the model for the next best question
            if turn < max_turns - 1:
                next_prompt = generate_next_prompt(conversation_history)
                if next_prompt:
                    logging.info(f"Next Prompt Suggestion: {next_prompt}")
                    prompt = next_prompt
                    conversation_history.append({"role": "user", "content": next_prompt})
                else:
                    logging.info("No next prompt generated. Ending conversation.")
                    break
        except Exception as e:
            logging.error(f"Error in conversation flow at turn {turn+1}: {e}")
            break
    return conversation_history

def main():
    logging.info("Starting LLaMA prompt processor...")
    prompts_dir = "prompts"
    output_dir = get_output_dir()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(prompts_dir).mkdir(parents=True, exist_ok=True)
    prompt_files = sorted(glob.glob(os.path.join(prompts_dir, "prompt_*.json")), key=os.path.getmtime, reverse=True)
    if not prompt_files:
        print("No prompt files found in 'prompts' directory. Please run 4.py to create a prompt.")
        return
    # Only process the most recent prompt file
    prompt_file = prompt_files[0]
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_data = json.load(f)
    prompt_id = prompt_data.get("id")
    prompt = prompt_data.get("prompt")
    if not prompt_id or not prompt:
        logging.warning(f"Skipping {prompt_file}: missing id or prompt.")
        return
    conversation_history = []
    conversation_history.append({"role": "user", "content": prompt})
    # You can adjust max_turns or other params here if needed
    conversation_history = advanced_conversation_flow(prompt, conversation_history, max_turns=1)
    # Save outputs with prompt_id in filenames
    save_conversation(conversation_history, filename=f"conversation_history_{prompt_id}.json")
    save_summary(conversation_history, filename=f"output_{prompt_id}.json")
    generate_markdown_summary(conversation_history, output_json_path=f"output_{prompt_id}.json", output_md_path=f"output_{prompt_id}.md")
    print(f"\nProcessed prompt {prompt_id}. Output files saved to: {os.path.abspath(output_dir)}")
    logging.info(f"Processed prompt {prompt_id} and saved outputs.")

if __name__ == "__main__":
    main()