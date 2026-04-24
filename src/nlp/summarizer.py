# NGO Field Report Summarizer
# This module extracts potential tasks from unstructured text reports.

import re

def extract_tasks_from_report(report_text):
    """
    Scans through text and finds sentences that contain "action" or "need" keywords.
    Returns a list of extracted task strings.
    """
    # 1. Split text into sentences (basic regex for . ! ?)
    sentences = re.split(r'(?<=[.!?]) +', report_text)
    
    extracted_tasks = []
    
    # 2. Keywords that suggest a task exists
    action_keywords = [
        "need", "required", "urgent", "shortage", "missing", 
        "request", "immediate", "delivery", "distribute", 
        "medical", "doctor", "medicine", "food", "rations", "water"
    ]
    
    for sentence in sentences:
        low_sentence = sentence.lower()
        # If the sentence has an action keyword, treat it as a task
        if any(keyword in low_sentence for keyword in action_keywords):
            # Clean up the sentence
            clean_task = sentence.strip()
            if len(clean_task) > 10: # Ignore very short strings
                extracted_tasks.append(clean_task)
                
    return extracted_tasks

def generate_report_summary(task_list):
    """
    Creates a high-level summary based on the tasks found.
    """
    if not task_list:
        return "No urgent needs identified in this report."
        
    return f"AI identified {len(task_list)} potential tasks that require your attention."
