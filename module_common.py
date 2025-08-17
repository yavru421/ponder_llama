import os
import json
import logging
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import requests

def atomic_write(file_path, data, mode='w', encoding='utf-8'):
    dir_name = os.path.dirname(file_path)
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode=mode, encoding=encoding, dir=dir_name, delete=False) as tf:
        tf.write(data)
        tempname = tf.name
    shutil.move(tempname, file_path)

def get_output_dir() -> str:
    return os.environ.get("PONDER_LLAMA_OUTPUT_DIR", "output")

def to_message_params(history: List[Dict[str, str]]) -> list:
    return history

def ddgs_search(query: str) -> Dict:
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"DDGS search failed: {e}")
        return {"error": str(e)}