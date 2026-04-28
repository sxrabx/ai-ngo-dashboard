import os
import json
from src.repository.volunteer_repository import VolunteerRepository
from src.core.gamifier import get_level_info

class VolunteerService:
    def __init__(self):
        self.repo = VolunteerRepository()
        # Path to static profiles
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.profiles_path = os.path.join(base_dir, 'data', 'sample_volunteers.json')

    def _load_profiles(self):
        if not os.path.exists(self.profiles_path):
            return []
        with open(self.profiles_path, 'r') as f:
            return json.load(f)

    def get_all_volunteers(self):
        """
        Merges static profile data with live performance stats (energy, levels).
        This is the 200-IQ single source of truth for the entire application.
        """
        profiles = self._load_profiles()
        stats = self.repo.load_all()

        for vol in profiles:
            v_id = vol['id']
            if v_id in stats:
                v_stats = stats[v_id]
                level, _ = get_level_info(v_stats.get('total_points', 0))
                vol['energy'] = v_stats.get('energy', 100)
                vol['current_level'] = level
                vol['total_points'] = v_stats.get('total_points', 0)
                vol['badges'] = v_stats.get('badges', [])
            else:
                # Default values for new volunteers not yet in stats
                vol['energy'] = 100
                vol['current_level'] = 1
                vol['total_points'] = 0
                vol['badges'] = []
        
        return profiles

    def update_after_mission(self, volunteer_id, points, category, energy_cost=25):
        """
        Updates volunteer stats via the repository.
        """
        # Note: Logic currently resides in gamifier.py, but we wrap it for consistency
        from src.core.gamifier import update_volunteer_after_task
        return update_volunteer_after_task(volunteer_id, points, category, energy_cost=energy_cost)

    def reset_all_energy(self):
        """Resets all energy levels to 100% via the repository."""
        return self.repo.reset_all_energy()
