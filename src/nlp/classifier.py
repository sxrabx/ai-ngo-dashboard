import json
import requests
import re
from config.settings import settings
from src.core.offline_engine import offline_intelligence_mode
import logging
import os

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/system.log',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)

NVIDIA_API_KEY = settings.NVIDIA_API_KEY
NVIDIA_API_URL = settings.NVIDIA_API_URL

# Global cache for the current session to prevent duplicate API calls
_llm_cache = {}

def call_llm(description, temperature=0.1, tone="Professional"):
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Analyze this disaster response report: "{description}"
    
    Extract:
    1. "intent": ["REPORT", "QUESTION"] - Is this a disaster report/incident or just a general question?
    2. "conversational_response": If intent is QUESTION, provide a helpful answer. If REPORT, keep it short like "Acknowledged."
    3. "thought_process": Your internal reasoning.
    4. "category": ["Health", "Relief", "Logistics", "Safety", "Mental Health", "Environment", "Admin", "Education", "General"]
    5. "urgency": ["Critical", "High", "Medium", "Low"]
    6. "people_count": Integer. IMPORTANT: Sum ALL individuals mentioned as needing help, trapped, or responsive. If multiple zones are mentioned, sum them.
    7. "understood_reasoning": A 2-3 sentence explanation as the AI Coordinator.
    
    EXTRACTION RULES:
    - If a report says "20 contractors, 13 made it out," the people_count is 7 (the ones trapped).
    - If a report mentions 100 in Zone A and 50 in Zone B, the people_count is 150.
    - If a report says "300 civilians safe but need water," they STILL COUNT towards people_count because they require logistics.
    
    TONE REQUIREMENT: Use a {tone} tone in the 'understood_reasoning' and 'thought_process'.
    
    Return ONLY a valid JSON object.
    """
    
    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        
        # Robust JSON extraction
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
            
        # Clean up common LLM JSON mistakes (like trailing commas)
        content = re.sub(r',\s*\}', '}', content)
        content = re.sub(r',\s*\]', ']', content)
        
        return json.loads(content)
    except Exception as e:
        # Log error to file
        logging.error(f"API failure. Switched to offline mode. Error: {str(e)}")
        
        with open("llm_error.log", "a") as f:
            f.write(f"Error: {str(e)}\nResponse: {getattr(response, 'text', 'N/A')}\n\n")
        
        print("LLM Error:", e)
        # Use Offline Fallback Engine
        return offline_intelligence_mode(description)

def get_cached_llm(description, temperature=0.1, tone="Professional"):
    if not description or len(description.strip()) < 3:
        return None
    
    # Cache key includes temperature and tone to ensure different results are cached
    cache_key = f"{description}_{temperature}_{tone}"
    if cache_key not in _llm_cache:
        _llm_cache[cache_key] = call_llm(description, temperature, tone)
    return _llm_cache[cache_key]

def get_intent(description, temperature=0.1, tone="Professional"):
    res = get_cached_llm(description, temperature, tone)
    return res.get("intent", "REPORT") if res else "REPORT"

def get_conversational_response(description, temperature=0.1, tone="Professional"):
    res = get_cached_llm(description, temperature, tone)
    return res.get("conversational_response", "I understand.") if res else "I'm processing that."

def classify_task(description, temperature=0.1, tone="Professional"):
    """
    Categorizes the task using NVIDIA NIM LLM.
    Returns: (category, initial_urgency)
    """
    res = get_cached_llm(description, temperature, tone)
    if res:
        cat = res.get("category", "General")
        if isinstance(cat, list) and len(cat) > 0:
            cat = cat[0] # Fallback to primary category
        elif not isinstance(cat, str):
            cat = str(cat)
            
        return cat, res.get("urgency", "Low")
    return "General", "Low"

def extract_impact_count(description, temperature=0.1, tone="Professional"):
    """
    Extracts people count using NVIDIA NIM LLM.
    """
    res = get_cached_llm(description, temperature, tone)
    if res and res.get("people_count") is not None:
        try:
            return int(res["people_count"])
        except (ValueError, TypeError):
            pass
    return None

def get_llm_reasoning(description, temperature=0.1, tone="Professional"):
    """
    Returns the reasoning string and internal thought process generated by the LLM.
    """
    res = get_cached_llm(description, temperature, tone)
    if res:
        summary = res.get("understood_reasoning", "I processed the request with standard AI algorithms.")
        thoughts = res.get("thought_process", "Thinking trace unavailable.")
        return summary, thoughts
    return "I processed the request with my standard algorithms.", "Trace not found."
