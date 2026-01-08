def calculate_score(
    vacancy_count: int,
    skills_found: int,
    *,
    max_vacancy_count: int,
    max_skills_possible: int,
    company_size_score: float,
    growth_score: float,
) -> float:

    vacancy_score = min(vacancy_count / max_vacancy_count, 1.0)
    skills_score = min(skills_found / max_skills_possible, 1.0)

    W_VACANCY = 0.25
    W_SKILLS = 0.45
    W_SIZE   = 0.15
    W_GROWTH = 0.15

    total = (
        vacancy_score * W_VACANCY +
        skills_score * W_SKILLS +
        company_size_score * W_SIZE +
        growth_score * W_GROWTH
    )

    return round(total * 100, 2)  # скор 0..100
