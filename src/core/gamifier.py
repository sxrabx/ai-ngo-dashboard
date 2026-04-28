from src.repository.volunteer_repository import VolunteerRepository

repo = VolunteerRepository()

def load_stats():
    """Loads volunteer stats via repository."""
    return repo.load_all()

def save_stats(stats):
    """Saves volunteer stats via repository."""
    repo.save_all(stats)

def calculate_reward_points(task_priority, volunteer_multiplier=1.0):
    """
    Calculates points based on task urgency and volunteer track record.
    High priority missions are now significantly more rewarding.
    """
    base_points = 50 # Minimum reward baseline
    
    # Priority scaling: High priority tasks (100) give up to 5x points (250 XP)
    multiplier = 1.0 + (task_priority / 20) 
    
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
    v_data = repo.get_by_id(volunteer_id)
    if v_data:
        current_energy = v_data.get("energy", 100)
        new_energy = max(0, current_energy - amount)
        repo.update_volunteer(volunteer_id, {"energy": new_energy})
        return new_energy
    return None

def recover_energy(volunteer_id, amount=5):
    """Increases volunteer energy during rest."""
    v_data = repo.get_by_id(volunteer_id)
    if v_data:
        current_energy = v_data.get("energy", 0)
        new_energy = min(100, current_energy + amount)
        repo.update_volunteer(volunteer_id, {"energy": new_energy})
        return new_energy
    return None


def update_volunteer_after_task(volunteer_id, task_points, category, energy_cost=25):
    """
    Updates a volunteer's stats after a task is assigned/completed.
    """
    v_data = repo.get_by_id(volunteer_id) or {"total_points": 0, "tasks_completed": 0, "badges": [], "categories": {}, "energy": 100}
    
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

    # 4. Dynamic Energy Depletion (Tactical Fatigue)
    v_data["energy"] = max(0, v_data.get("energy", 100) - energy_cost)
    
    repo.update_volunteer(volunteer_id, v_data)
    return v_data, new_badges

def bulk_update_volunteers_after_task(volunteer_ids, task_points, category, energy_cost=25):
    """
    Performs a high-performance bulk update for multiple volunteers to prevent I/O bottlenecks.
    """
    all_stats = repo.load_all()
    updates = {}
    
    for v_id in volunteer_ids:
        v_data = all_stats.get(v_id, {
            "total_points": 0, 
            "tasks_completed": 0, 
            "badges": [], 
            "categories": {}, 
            "energy": 100
        })
        v_data["total_points"] += task_points
        v_data["tasks_completed"] += 1
        cat_stats = v_data.get("categories", {})
        cat_stats[category] = cat_stats.get(category, 0) + 1
        v_data["categories"] = cat_stats
        v_data["energy"] = max(0, v_data.get("energy", 100) - energy_cost)
        if v_data["total_points"] >= 500 and "Veteran" not in v_data["badges"]:
            v_data["badges"].append("Veteran")
        updates[v_id] = v_data
    return repo.bulk_update(updates)


