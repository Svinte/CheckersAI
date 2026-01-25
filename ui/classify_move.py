def classify_move(delta, avg):
    # Move quality
    if delta > 1.5:
        quality = "Excellent"
    elif delta > 0.5:
        quality = "Good"
    elif delta > -0.3:
        quality = "Neutral"
    elif delta > -1.0:
        quality = "Poor"
    else:
        quality = "Terrible"

    # Comparison vs average
    diff = delta - avg
    if diff >= 1.0:
        comparison = "Best possible"
    elif diff >= 0.8:
        comparison = "Great"
    elif diff >= 0.2:
        comparison = "Slightly better"
    elif diff >= -0.2:
        comparison = "About average"
    elif diff >= -0.8:
        comparison = "Slightly worse"
    else:
        comparison = "Much worse"

    # Combined single output
    if quality == "Excellent" and comparison in ("Best possible", "Great"):
        return "Incredible"
    if quality == "Excellent" and comparison == "Slightly better":
        return "Very strong"
    if quality == "Good" and comparison in ("Best possible", "Great"):
        return "Very good"
    if quality == "Good" and comparison == "Slightly better":
        return "Good"
    if quality == "Neutral" and comparison in ("About average", "Slightly better"):
        return "Okay"
    if quality == "Neutral" and comparison in ("Slightly worse", "Much worse"):
        return "Not good"
    if quality == "Poor" and comparison in ("Slightly worse", "Much worse"):
        return "Bad"
    if quality == "Terrible" and comparison in ("Slightly worse", "Much worse"):
        return "Worst case"

    # Fallback
    return f"{quality} ({comparison})"
