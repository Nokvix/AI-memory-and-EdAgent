"""
Добавление тестовой компании для проверки эндпоинтов
"""

from app.core.database import SessionLocal
from app.models.models import Company

db = SessionLocal()

# Проверяем, есть ли уже компании
existing = db.query(Company).first()

if not existing:
    # Создаём тестовую компанию
    test_company = Company(
        name="ООО Контур",
        url="https://hh.ru/employer/41862",
        industry="IT",
        score=92.0,
        vacancy_count=12,
        main_skills=["Python", "Django", "PostgreSQL", "Docker", "REST API"],
        status="new"
    )
    db.add(test_company)
    db.commit()
    print(f"✅ Создана тестовая компания: {test_company.name} (ID: {test_company.id})")
else:
    print(f"✅ Компания уже существует: {existing.name} (ID: {existing.id})")

db.close()
