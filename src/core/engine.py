from src.nlp.classifier import classify_task, extract_impact_count, get_llm_reasoning, get_intent, get_conversational_response
from src.core.matcher import find_matches
from src.core.scorer import calculate_score
from src.core.gamifier import calculate_reward_points, load_stats, get_level_info

def assemble_squad(priority, volunteers, category, people_count):
    """
    Properly scales team size and composition based on people_affected.
    Ratio: ~1 Specialist per 2 affected people for Critical, 1 per 5 for Medium.
    """
    # 1. Determine Manpower Requirements
    if priority >= 100: ratio = 1.0 # 1-to-1 response for absolute criticals
    elif priority > 80: ratio = 2.0
    elif priority > 60: ratio = 4.0
    else: ratio = 8.0
    
    required_count = max(4, round(people_count / ratio))
    
    # Cap squad size at 48 for mass disasters (split across teams)
    required_count = min(48, required_count)
    
    squad = sorted(volunteers, key=lambda x: x.get('match_score', 0), reverse=True)
    final_pool = squad[:required_count]
    
    # 2. Assign Team Tiers based on scale
    if required_count >= 12:
        tier = "REGIMENT"
        # Split into 4 specialized teams
        chunk = required_count // 4
        return {
            "is_split": True, 
            "tier": tier, 
            "required_manpower": required_count,
            "team_alpha": final_pool[:chunk], # Extraction/Breach
            "team_beta": final_pool[chunk:chunk*2], # Medical/Safety
            "team_gamma": final_pool[chunk*2:chunk*3], # Logistics/Supply
            "team_delta": final_pool[chunk*3:] # Perimeter/Support
        }
    elif required_count >= 6:
        tier = "STRIKE FORCE"
        return {
            "is_split": True, 
            "tier": tier, 
            "required_manpower": required_count,
            "team_alpha": final_pool[:round(required_count/2)], 
            "team_beta": final_pool[round(required_count/2):]
        }
    
    return {
        "is_split": False,
        "tier": "RESCUE CELL",
        "required_manpower": required_count,
        "team_alpha": final_pool
    }

def process_new_task(task_data, all_volunteers, tone="Professional", temperature=0.4):
    desc = task_data['description']
    intent = get_intent(desc, temperature=temperature, tone=tone)
    conv_res = get_conversational_response(desc, temperature=temperature, tone=tone)
    
    if intent == "QUESTION":
        return {
            "intent": "QUESTION",
            "message": conv_res,
            "ai_reasoning": {"understood": conv_res, "raw_thinking": "User asked a direct question."}
        }

    category, urgency = classify_task(desc, temperature=temperature, tone=tone)
    extracted_count = extract_impact_count(desc, temperature=temperature, tone=tone)
    people_count = extracted_count if extracted_count is not None else task_data.get('people_count', 1)
    priority = calculate_score(urgency, people_count)
    
    stats = load_stats()
    for v in all_volunteers:
        v_id = v.get('id')
        if v_id in stats:
            level, _ = get_level_info(stats[v_id]['total_points'])
            v['current_level'] = level
            v['energy'] = stats[v_id].get('energy', 100)
            v['total_points'] = stats[v_id].get('total_points', 0)
        else:
            v['current_level'] = 1; v['energy'] = 100; v['total_points'] = 0

    volunteers_with_scores = find_matches(desc, category, (0,0), all_volunteers)
    potential_points = calculate_reward_points(priority)
    recommended_squad = assemble_squad(priority, volunteers_with_scores, category, people_count)
    
    squad_ids = set()
    if isinstance(recommended_squad, dict):
        for team in ['team_alpha', 'team_beta', 'team_gamma']:
            for v in recommended_squad.get(team, []): squad_ids.add(v['id'])
    else:
        for v in recommended_squad: squad_ids.add(v['id'])
    
    alternatives = [v for v in volunteers_with_scores if v['id'] not in squad_ids][:6]
    explanation, raw_thinking = get_llm_reasoning(desc, temperature=temperature, tone=tone)

    return {
        "intent": "REPORT",
        "task_id": task_data['task_id'],
        "category": category,
        "priority_score": priority,
        "urgency_level": urgency,
        "people_count": people_count,
        "recommended_squad": recommended_squad,
        "top_alternatives": alternatives,
        "potential_reward_points": potential_points,
        "ai_reasoning": {"understood": explanation, "action": "Units Deployed.", "raw_thinking": raw_thinking}
    }


