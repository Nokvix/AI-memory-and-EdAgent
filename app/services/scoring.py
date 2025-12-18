def calculate_score(vacancy_count: int, skills_found: int) -> float:
    raw_score = (vacancy_count * 5) + (skills_found * 10)
    return float(raw_score)
