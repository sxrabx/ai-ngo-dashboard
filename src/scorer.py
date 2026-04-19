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
    # Reverted logic: +2 points per person, capped at +30 bonus
    impact_bonus = min(30, people_affected * 2)
    score += impact_bonus
    
    return min(score, 100) # Strictly capped at 100
