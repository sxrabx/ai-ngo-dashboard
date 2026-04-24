import math
import sys
import os

# New vector DB integration for Option 2+3
try:
    from src.nlp.vector_db import init_volunteer_db, query_semantic_match
except ImportError:
    # Handle if run directly
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.nlp.vector_db import init_volunteer_db, query_semantic_match

def calculate_distance(pos1, pos2):
    """
    Calculates Euclidean distance between two (x, y) coordinates.
    """
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def find_matches(task_description, category, task_location, volunteers):
    """
    Ranks volunteers based on a weighted Match Score:
    - Semantic Match (ChromaDB + Sentence Transformers): Up to +60 points
    - Fallback Keyword Skill Match: +30 points
    - Availability: +30 points
    - Proximity: Up to +20 points (closer is better)
    """
    # Initialize / Sync the Vector DB with current active volunteers
    init_volunteer_db(volunteers)
    
    # Query ChromaDB for top 10 closest semantic matches
    top_semantic_ids = query_semantic_match(task_description, n_results=10)
    
    scored_volunteers = []
    
    for v in volunteers:
        # 0. Sustainability Filter: Skip exhausted volunteers
        if v.get('energy', 100) <= 0:
            continue

        score = 0
        v_id = str(v.get('id', ''))
        
        # 1. AI SEMANTIC MATCHING (Primary Weight: Max 60)
        if v_id in top_semantic_ids:
            # The closer they are to index 0, the more accurate the match
            rank = top_semantic_ids.index(v_id)
            score += max(20, 60 - (rank * 5))  # e.g. Rank 0 gets 60 pts, Rank 1 gets 55 pts...
        elif category in v.get('skills', []):
            # Fallback to strict keyword matching if not found by AI
            score += 30
            
        # 2. Availability (Weight: 30)
        if v.get('available', False):
            score += 30
            
        # 3. Proximity (Weight: 10)
        if 'location_coords' in v and task_location:
            dist = calculate_distance(v['location_coords'], task_location)
            # Give more points for smaller distances
            proximity_score = max(0, 10 - dist) 
            score += proximity_score
        
        # 4. Energy Penalty (Subtle bias towards fresh volunteers)
        energy_bonus = (v.get('energy', 100) / 100) * 5
        score += energy_bonus

        # 5. Final Safety Cap at 100
        score = min(100, score)
        
        # Store the calculated score in the volunteer object for the output
        v_copy = v.copy()
        v_copy['match_score'] = round(score, 2)
        scored_volunteers.append(v_copy)


    # Sort volunteers: Highest score first
    ranked_list = sorted(scored_volunteers, key=lambda x: x['match_score'], reverse=True)
            
    # --- SMART TRIAGE: Identify Fastest Responder ---
    if ranked_list:
        # Sort internal copy by distance to find the absolute closest
        closest = min(scored_volunteers, key=lambda x: calculate_distance(x.get('location_coords', (0,0)), task_location))
        closest_dist = calculate_distance(closest.get('location_coords', (0,0)), task_location)
        
        # Mark them as fast responder if they are significantly closer than the lead
        top_match = ranked_list[0]
        top_dist = calculate_distance(top_match.get('location_coords', (0,0)), task_location)
        
        if closest_dist < top_dist * 0.5: # 50% closer
            # Find the index of the closest in the ranked list and tag them
            for v in ranked_list:
                if v['id'] == closest['id']:
                    v['is_fast_responder'] = True
                    break

    return ranked_list


# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    # Mock Data
    dummy_volunteers = [
        {"name": "Alice", "skills": ["Health"], "location_coords": (0, 0), "available": True},
        {"name": "Bob", "skills": ["Health"], "location_coords": (50, 50), "available": True}
    ]
    
    # Task is at (1, 1)
    results = find_matches("Health", (1, 1), dummy_volunteers)
    
    print("Match Results:")
    for v in results:
        print(f"- {v['name']}: Score {v['match_score']}")
