from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.models import Company, Vacancy
from app.services.scoring import calculate_score

Base.metadata.create_all(bind=engine)


def import_data():
    db = SessionLocal()

    fake_data = [
        {
            "name": "ООО Контур", "url": "hh.ru/1", "industry": "IT",
            "vacancies": [
                {"pos": "Python Dev", "skills": ["Python", "SQL"]},
                {"pos": "React Dev", "skills": ["JS", "React"]}
            ]
        },
        {
            "name": "Завод №5", "url": "hh.ru/2", "industry": "Industrial",
            "vacancies": [{"pos": "Manager", "skills": ["Excel"]}]
        }
    ]

    print("Импорт данных...")
    for data in fake_data:
        all_skills = []
        for v in data["vacancies"]:
            all_skills.extend(v["skills"])
        unique_skills = list(set(all_skills))

        score = calculate_score(len(data["vacancies"]), len(unique_skills))

        company = Company(
            name=data["name"],
            url=data["url"],
            industry=data["industry"],
            vacancy_count=len(data["vacancies"]),
            main_skills=unique_skills,
            score=score
        )
        db.add(company)
        db.commit()
        db.refresh(company)

        for v in data["vacancies"]:
            vac = Vacancy(company_id=company.id, position=v["pos"], skills=v["skills"], url="...")
            db.add(vac)

    db.commit()
    print("Импорт завершен!")
    db.close()


if __name__ == "__main__":
    import_data()