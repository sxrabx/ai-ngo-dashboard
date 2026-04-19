import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'volunteer_stats.json')

def load_stats():
    """Loads volunteer stats from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_stats(stats):
    """Saves volunteer stats to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

def calculate_reward_points(task_priority, volunteer_multiplier=1.0):
    """
    Calculates points based on task urgency and volunteer track record.
    """
    base_points = 20 # Minimum points for any task
    
    # Priority scaling: High priority tasks give up to 2x points
    multiplier = 1.0 + (task_priority / 100)
    
    final_points = int(base_points * multiplier * volunteer_multiplier)
    return final_points

def get_level_info(points):
    """
    Calculates level and progress to next level based on a simple log scale.
    """
    level = (points // 100) + 1
    progress = points % 100
    return level, progress

def deplete_energy(volunteer_id, amount=25):
    """Reduces volunteer energy after a mission."""
    stats = load_stats()
    if volunteer_id in stats:
        stats[volunteer_id]["energy"] = max(0, stats[volunteer_id].get("energy", 100) - amount)
        save_stats(stats)
        return stats[volunteer_id]["energy"]
    return None

def recover_energy(volunteer_id, amount=10):
    """Increases volunteer energy during rest."""
    stats = load_stats()
    if volunteer_id in stats:
        stats[volunteer_id]["energy"] = min(100, stats[volunteer_id].get("energy", 0) + amount)
        save_stats(stats)
        return stats[volunteer_id]["energy"]
    return None


def update_volunteer_after_task(volunteer_id, task_points, category):
    """
    Updates a volunteer's stats after a task is assigned/completed.
    """
    stats = load_stats()
    
    if volunteer_id not in stats:
        stats[volunteer_id] = {"total_points": 0, "tasks_completed": 0, "badges": [], "categories": {}}

    v_data = stats[volunteer_id]
    v_data["total_points"] += task_points
    v_data["tasks_completed"] += 1
    
    # Update category-specific count
    cat_stats = v_data.get("categories", {})
    cat_stats[category] = cat_stats.get(category, 0) + 1
    v_data["categories"] = cat_stats
    
    # Simple Badge Logic
    new_badges = []
    if v_data["total_points"] >= 500 and "Veteran" not in v_data["badges"]:
        new_badges.append("Veteran")
    if v_data["tasks_completed"] >= 10 and "Dedicated" not in v_data["badges"]:
        new_badges.append("Dedicated")
    if cat_stats.get("Health", 0) >= 5 and "Medical Hero" not in v_data["badges"]:
        new_badges.append("Medical Hero")
    
    v_data["badges"].extend(new_badges)

    # 4. Energy Depletion (Integrated Sustainability)
    v_data["energy"] = max(0, v_data.get("energy", 100) - 25)
    
    save_stats(stats)
    return v_data, new_badges

