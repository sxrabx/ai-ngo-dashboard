import json
import os
import threading

class VolunteerRepository:
    _lock = threading.RLock()

    def __init__(self, file_path=None):
        if file_path is None:
            # Absolute path resolution to prevent CWD dependency issues
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.file_path = os.path.join(base_dir, 'data', 'volunteer_stats.json')
        else:
            self.file_path = file_path

    def load_all(self):
        """Loads all volunteer stats with thread safety."""
        with self._lock:
            return self._load_no_lock()

    def _load_no_lock(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return {}
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_all(self, stats):
        """Saves all volunteer stats with thread safety."""
        with self._lock:
            self._save_no_lock(stats)

    def _save_no_lock(self, stats):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # Write to a temporary file first then rename to ensure atomic write
        temp_file = self.file_path + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(stats, f, indent=4)
        os.replace(temp_file, self.file_path)

    def get_by_id(self, volunteer_id):
        """Gets stats for a specific volunteer."""
        stats = self.load_all()
        return stats.get(volunteer_id)

    def update_volunteer(self, volunteer_id, updates):
        """Atomic update for a specific volunteer's stats."""
        with self._lock:
            stats = self._load_no_lock()
            if volunteer_id not in stats:
                stats[volunteer_id] = {
                    "total_points": 0, 
                    "tasks_completed": 0, 
                    "badges": [], 
                    "categories": {}, 
                    "energy": 100
                }
            
            stats[volunteer_id].update(updates)
            self._save_no_lock(stats)
            return stats[volunteer_id]
    def reset_all_energy(self):
        """Restores all volunteers to 100% energy."""
        with self._lock:
            stats = self._load_no_lock()
            for v_id in stats:
                stats[v_id]['energy'] = 100
            self._save_no_lock(stats)
            return True
    def bulk_update(self, volunteer_updates):
        """
        Updates multiple volunteers in a single atomic operation.
        volunteer_updates: Dict of {id: {stats_dict}}
        """
        with self._lock:
            stats = self._load_no_lock()
            for v_id, updates in volunteer_updates.items():
                if v_id not in stats:
                    stats[v_id] = {
                        "total_points": 0, 
                        "tasks_completed": 0, 
                        "badges": [], 
                        "categories": {}, 
                        "energy": 100
                    }
                stats[v_id].update(updates)
            self._save_no_lock(stats)
        return True
