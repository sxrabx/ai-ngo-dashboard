import sys
import os

# Add the 'src' directory to the path so we can import our modules
# Add the root directory to the path so we can import 'src' as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import process_new_task

# --- MOCK DATA FOR TESTING ---

mock_volunteers = [
    {
        "id": "V001",
        "name": "Arjun (Doctor - Far)",
        "skills": ["Health"],
        "location_coords": (10, 10), # Far away
        "available": True
    },
    {
        "id": "V002",
        "name": "Priya (Doctor - Close)",
        "skills": ["Health"],
        "location_coords": (1, 1), # Very close
        "available": True
    },
    {
        "id": "V003",
        "name": "Rahul (General - Busy)",
        "skills": ["Health"],
        "location_coords": (0, 1), # Very close but busy
        "available": False
    }
]

test_task = {
    "task_id": "T404",
    "description": "Critical medical assistance needed at the clinic.",
    "people_count": 10,
    "location_coords": (0, 0) # Task is at origin
}

# --- RUNNING THE TEST ---

print("="*40)
print("RUNNING AI LOGIC TEST")
print("="*40)

print(f"TASK: {test_task['description']}")
print("-" * 20)

result = process_new_task(test_task, mock_volunteers)

print(f"CATEGORY identified: {result['category']}")
print(f"URGENCY level:      {result['urgency_level']}")
print(f"PRIORITY SCORE:     {result['priority_score']}/100")
print("-" * 20)

print(f"FOUND {len(result['suggested_volunteers'])} RANKED VOLUNTEERS:")
for v in result['suggested_volunteers']:
    print(f"- {v['name']:<25} | Score: {v['match_score']}/100")

print("="*40)
print("TEST COMPLETED")
