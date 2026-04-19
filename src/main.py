# Entry point for the AI Intelligence Layer
from src.classifier import classify_task, extract_impact_count, get_llm_reasoning


from src.scorer import calculate_score
from src.matcher import find_matches
from src.gamifier import calculate_reward_points, load_stats, get_level_info


def assemble_squad(priority_score, ranked_volunteers, category, people_count=1):
    """
    Refined Logic: Dynamic Squad Sizing + Mega-Squad Splitting
    """
    # 1. Calculate Dynamic Target Size
    # Scaling: 1 per 5 people. Max 10 per squad.
    target_size = max(4, min(20 if people_count > 40 else 10, (people_count // 5) + 2))
    
    # 2. Separate by experience
    experts = [v for v in ranked_volunteers if v.get('current_level', 1) >= 4]
    rookies = [v for v in ranked_volunteers if v.get('current_level', 1) < 4]
    cat_specialists = [v for v in ranked_volunteers if category in v.get('skills', [])]
    
    squad = []
    
    # 3. Dynamic Expansion (Build the pool)
    relevant_experts = [v for v in experts if (v.get('match_score', 0) >= 40 or category in v.get('skills', []))]
    relevant_rookies = [v for v in rookies if (v.get('match_score', 0) >= 40 or category in v.get('skills', []))]
    
    # First, pick leads
    leads = []
    if cat_specialists:
        leads = [v for v in cat_specialists if v.get('current_level', 1) >= 3]
        if not leads: leads = [cat_specialists[0]]
    elif experts:
        leads = experts[:2]
    
    if leads:
        squad.append(leads[0])
        if len(leads) > 1 and people_count > 40:
            squad.append(leads[1]) # Reserve second lead for Team Beta
            
    # Fill the rest
    remaining = [v for v in ranked_volunteers if v not in squad and v.get('match_score', 0) >= 30]
    while len(squad) < target_size and remaining:
        squad.append(remaining.pop(0))
    
    final_pool = squad[:target_size]

    # 4. MEGA-SQUAD SPLIT LOGIC
    if people_count > 40 and len(final_pool) >= 8:
        # Split into Alpha and Beta
        mid = len(final_pool) // 2
        team_alpha = final_pool[:mid]
        team_beta = final_pool[mid:]
        
        return {
            "type": "MEGA_SQUAD",
            "is_split": True,
            "team_alpha": team_alpha,
            "team_beta": team_beta,
            "total_count": len(final_pool)
        }
    
    return final_pool


def process_new_task(task_data, all_volunteers):
    """
    Main pipeline: Classify -> Score -> Match -> Gamify -> Squad Assembly
    """
    # 1. Classify
    category, urgency = classify_task(task_data['description'])
    
    # 2. Extract Impact Count if not provided or to verify
    extracted_count = extract_impact_count(task_data['description'])
    people_count = extracted_count if extracted_count is not None else task_data.get('people_count', 1)

    # 3. Score
    priority = calculate_score(urgency, people_count)

    
    # 3. Inject Stats (Energy/Level) into data before matching
    stats = load_stats()
    for v in all_volunteers:
        v_id = v.get('id')
        if v_id in stats:
            level, _ = get_level_info(stats[v_id]['total_points'])
            v['current_level'] = level
            v['current_badges'] = stats[v_id]['badges']
            v['energy'] = stats[v_id].get('energy', 100)
        else:
            v['current_level'] = 1
            v['current_badges'] = []
            v['energy'] = 100

    # 4. Match (Now with Energy & Semantic Awareness)
    location = task_data.get('location_coords', (0,0))
    volunteers = find_matches(task_data['description'], category, location, all_volunteers)
    
    # 5. Gamify Intelligence
    potential_points = calculate_reward_points(priority)
            
    # 6. Squad Assembly (The Hybrid Logic)
    recommended_squad = assemble_squad(priority, volunteers, category, people_count)

    # 7. Generate "What I Understood" Detailed Analysis from LLM
    explanation_req, raw_thinking = get_llm_reasoning(task_data['description'])

    
    # Selection Rationale
    is_mega = isinstance(recommended_squad, dict) and recommended_squad.get('is_split', False)
    if is_mega:
        action_done = (
            f"Due to the massive scale ({people_count} victims), I implemented a **Multi-Lead deployment**. "
            f"I split the resources into **Team Alpha** and **Team Beta** to prevent management bottleneck and ensure the specialized leadership of two veteran volunteers."
        )
    else:
        lead = recommended_squad[0] if recommended_squad else None
        lead_reason = "skill seniority" if lead and lead['current_level'] > 5 else "proximity/response-time"
        action_done = (
            f"I matched your request with a precision squad of **{len(recommended_squad)} responders**. "
            f"I designated **{lead['name'] if lead else 'N/A'}** as Lead because of their high **{lead_reason}**. "
            f"I also verified the energy level of all selected units (Average: **{int(sum(m['energy'] for m in recommended_squad)/len(recommended_squad)) if recommended_squad else 0}%**) to ensure mission sustainability."
        )

    reasoning = {
        "understood": explanation_req,
        "action": action_done,
        "raw_thinking": raw_thinking
    }
    
    return {
        "task_id": task_data['task_id'],
        "category": category,
        "priority_score": priority,
        "urgency_level": urgency,
        "people_count": people_count,
        "suggested_volunteers": volunteers,
        "recommended_squad": recommended_squad,
        "potential_reward_points": potential_points,
        "ai_reasoning": reasoning
    }




if __name__ == "__main__":
    print("AI Intelligence Layer Initialized.")
    # Example usage:
    # result = process_new_task({...}, [...])
