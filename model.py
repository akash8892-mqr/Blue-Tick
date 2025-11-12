import re
import random

def predict_fake_probability(url: str) -> float:
    """
    Placeholder model — replace with your ML pipeline later
    Returns probability between 0 and 1
    """

    # Simple pattern checks for now
    score = 0

    # suspicious usernames
    sus_patterns = [
        r"\d{4,}",     # many numbers
        r"free",
        r"bot",
        r"follow",
        r"official\d+",
        r"gift"
    ]

    for p in sus_patterns:
        if re.search(p, url.lower()):
            score += 0.3

    # unknown social domain => suspicious
    if not any(s in url.lower() for s in ["instagram.com", "linkedin.com"]):
        score += 0.2

    # keep score in range
    score = max(0, min(score, 0.95))

    # slight randomness to simulate ML behavior
    score += random.uniform(-0.05, 0.05)
    score = max(0, min(score, 1))

    return score
