def calculate_score(vacancy_count: int, skills_found: int) -> float:
    raw_score = (vacancy_count * 10 + skills_found * 20)
    return min(float(raw_score), 100.0)
