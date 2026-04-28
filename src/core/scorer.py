def calculate_score(urgency, people_affected):
    """
    Returns a numerical score between 1 and 100.
    100 = Highest Priority, 1 = Lowest Priority
    """
    # Base importance by urgency label (reverted to 100 scale)
    base_scores = {"Critical": 90, "High": 70, "Medium": 40, "Low": 10}
    
    # Normalize input and calculate base
    norm_urgency = str(urgency).strip().capitalize()
    score = base_scores.get(norm_urgency, 10)
    
    # Impact Factor: Add points based on people affected
    # Aggressive scaling: +5 points per 10 people, plus 1 point per person for smaller groups
    if people_affected > 100:
        impact_bonus = 60 # Massive impact
    elif people_affected > 50:
        impact_bonus = 40
    else:
        impact_bonus = people_affected * 1.5
        
    score += impact_bonus
    
    return min(100, int(score)) # Strictly capped at 100
