import json
import os
from collections import defaultdict
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.models import Company, Vacancy
from app.services.scoring import calculate_score

Base.metadata.create_all(bind=engine)


def load_json_data(filename):
    possible_paths = [
        filename,
        f"parsers/hh/{filename}",
        f"parsers/superjob/{filename}"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Файл найден: {path}")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка чтения файла {path}: {e}")
                return []

    print(f"Файл {filename} не найден ни в одной из папок.")
    return []


def extract_skills_from_vac_list(vac_list):
    all_skills = []
    for v in vac_list:
        skills = v.get("main_skills", [])
        if isinstance(skills, list):
            all_skills.extend(skills)
        elif isinstance(skills, str):
            all_skills.append(skills)
    return list(set(all_skills))


def import_data():
    db: Session = SessionLocal()

    sj_data = load_json_data("superjob_vacancies.json")
    hh_data = load_json_data("vacancies.json")

    all_vacancies = sj_data + hh_data

    if not all_vacancies:
        print("Нет данных для импорта. Проверь наличие .json файлов.")
        return

    print(f"Всего вакансий для обработки: {len(all_vacancies)}")

    companies_map: dict[str, list[dict]] = defaultdict(list)

    for item in all_vacancies:
        raw_name = item.get("company_name")

        if raw_name:
            comp_name = str(raw_name).strip()
        else:
            comp_name = "Неизвестная компания"

        if not comp_name:
            comp_name = "Неизвестная компания"

        companies_map[comp_name].append(item)

    print(f"Найдено уникальных компаний: {len(companies_map)}")

    max_vacancy_count = 0
    max_skills_possible = 0

    for comp_name, vac_list in companies_map.items():
        vacancy_count = len(vac_list)
        unique_skills = extract_skills_from_vac_list(vac_list)

        if vacancy_count > max_vacancy_count:
            max_vacancy_count = vacancy_count

        skills_count = len(unique_skills)
        if skills_count > max_skills_possible:
            max_skills_possible = skills_count

    if max_vacancy_count == 0:
        max_vacancy_count = 1
    if max_skills_possible == 0:
        max_skills_possible = 1

    print(f"max_vacancy_count = {max_vacancy_count}")
    print(f"max_skills_possible = {max_skills_possible}")

    count_new_companies = 0

    for comp_name, vac_list in companies_map.items():
        existing_company = (
            db.query(Company)
            .filter(Company.name == comp_name)
            .first()
        )

        if existing_company:
            company = existing_company
        else:
            unique_skills = extract_skills_from_vac_list(vac_list)
            first_vac = vac_list[0]

            url = first_vac.get("company_url") or ""

            vacancy_count = len(vac_list)
            skills_count = len(unique_skills)

            # Здесь как раз второй вариант: передаём keyword-only аргументы
            score = calculate_score(
                vacancy_count,
                skills_count,
                max_vacancy_count=max_vacancy_count,
                max_skills_possible=max_skills_possible,
                company_size_score=0.5,
                growth_score=0.5,
            )

            company = Company(
                name=comp_name,
                url=url,
                industry="IT / Промышленность / Другое",
                vacancy_count=vacancy_count,
                main_skills=unique_skills,
                score=score,
                status="new",
            )
            db.add(company)
            db.flush()
            count_new_companies += 1

        for v in vac_list:
            vac_url = v.get("vacancy_url")
            if vac_url and db.query(Vacancy).filter(Vacancy.url == vac_url).first():
                continue

            vacancy = Vacancy(
                company_id=company.id,
                position=v.get("position", "Не указана"),
                skills=v.get("main_skills", []),
                url=vac_url or "",
            )
            db.add(vacancy)

    db.commit()
    db.close()
    print(f"Импорт завершен! Добавлено новых компаний: {count_new_companies}")


if __name__ == "__main__":
    import_data()
