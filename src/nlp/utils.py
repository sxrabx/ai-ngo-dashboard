import json
import re
import logging

def clean_json_string(raw_str):
    """
    Cleans common LLM JSON errors:
    1. Removes markdown code blocks (```json ... ```)
    2. Removes trailing commas (e.g., "key": "value", })
    3. Trims whitespace
    """
    if not raw_str:
        return ""
        
    # Remove markdown code blocks
    clean_str = re.sub(r'```json\s*', '', raw_str)
    clean_str = re.sub(r'```\s*', '', clean_str)
    
    # Extract only the content between the first { and last }
    json_match = re.search(r'\{.*\}', clean_str, re.DOTALL)
    if json_match:
        clean_str = json_match.group(0)
    
    # Remove trailing commas from objects and arrays
    clean_str = re.sub(r',\s*\}', '}', clean_str)
    clean_str = re.sub(r',\s*\]', ']', clean_str)
    
    return clean_str.strip()

def safe_json_loads(raw_str, fallback=None):
    """
    Safely loads JSON with error handling and cleaning.
    """
    cleaned = clean_json_string(raw_str)
    try:
        return json.loads(cleaned)
    except Exception as e:
        logging.error(f"JSON Parsing Error: {e}\nRaw: {raw_str}\nCleaned: {cleaned}")
        return fallback
