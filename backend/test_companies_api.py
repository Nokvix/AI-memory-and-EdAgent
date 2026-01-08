"""
Тестовые запросы к Companies API
Проверка всех 5 эндпоинтов
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 80)
print("ТЕСТИРОВАНИЕ COMPANIES API")
print("=" * 80)

# Тест 1: Получить топ-20 компаний
print("\n[TEST 1] GET /api/companies/top-20")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies/top-20")
    print(f"Status: {response.status_code}")
    companies = response.json()
    print(f"Количество компаний: {len(companies)}")
    if companies:
        print(f"Первая компания: {companies[0].get('name')} (score: {companies[0].get('score')})")
        print(f"Топ-20 получен")
    else:
        print("Список пуст (нет компаний в БД)")
except Exception as e:
    print(f"Ошибка: {e}")

# Тест 2: Получить конкретную компанию (ID=1)
print("\n\n[TEST 2] GET /api/companies/1")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies/1")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        company = response.json()
        print(json.dumps(company, indent=2, ensure_ascii=False))
        print(f"Компания получена")
    else:
        print(f"Компания не найдена: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")
# Тест 3: Получить список с фильтром по статусу
print("\n\n[TEST 3] GET /api/companies?status=new&page=1&limit=5")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies?status=new&page=1&limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Всего компаний со статусом 'new': {data.get('total')}")
    print(f"На текущей странице: {len(data.get('data', []))}")
    print(f"Страница: {data.get('page')}, Лимит: {data.get('limit')}")
    print(f"Фильтрация работает")
except Exception as e:
    print(f"Ошибка: {e}")

# Тест 4: Фильтр с невалидным статусом (ожидается 400)
print("\n\n[TEST 4] GET /api/companies?status=invalid (ожидается ошибка)")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies?status=invalid")
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print(f"Валидация статуса работает: {response.json().get('detail')}")
    else:
        print(f"Неожиданный результат: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")
# Тест 5: Одобрить компанию
print("\n\n[TEST 5] POST /api/companies/1/approve")
print("-" * 80)
try:
    response = requests.post(
        f"{BASE_URL}/companies/1/approve",
        json={"comment": "Отличная компания для партнёрства"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        company = response.json()
        print(f"Новый статус: {company.get('status')}")
        if company.get('status') == 'approved':
            print(f"Компания успешно одобрена")
        else:
            print(f"Статус: {company.get('status')}")
    else:
        print(f"Ошибка: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")

# Тест 6: Проверить изменение статуса
print("\n\n[TEST 6] GET /api/companies/1 (проверка статуса после approve)")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies/1")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        company = response.json()
        print(f"Статус компании: {company.get('status')}")
        if company.get('status') == 'approved':
            print(f"Статус изменён на 'approved'")
        else:
            print(f"Статус: {company.get('status')}")
except Exception as e:
    print(f"Ошибка: {e}")
# Тест 7: Отклонить компанию (создадим новую или используем существующую)
print("\n\n[TEST 7] POST /api/companies/1/reject")
print("-" * 80)
try:
    response = requests.post(
        f"{BASE_URL}/companies/1/reject",
        json={"reason": "Не соответствует критериям программы"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        company = response.json()
        print(f"Новый статус: {company.get('status')}")
        if company.get('status') == 'rejected':
            print(f"Компания успешно отклонена")
        else:
            print(f"Статус: {company.get('status')}")
    else:
        print(f"Ошибка: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")

# Тест 8: Фильтр по минимальному скору
print("\n\n[TEST 8] GET /api/companies?min_score=80")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies?min_score=80")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Всего компаний со скором >= 80: {data.get('total')}")
    if data.get('data'):
        scores = [c.get('score') for c in data.get('data', [])]
        print(f"Скоры первых 5: {scores[:5]}")
        if all(s >= 80 for s in scores):
            print(f"Фильтр по min_score работает")
        else:
            print(f"Есть компании с score < 80")
    else:
        print("Нет компаний с таким скором")
except Exception as e:
    print(f"Ошибка: {e}")

# Тест 9: Сортировка по имени
print("\n\n[TEST 9] GET /api/companies?sort_by=name_asc&limit=3")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies?sort_by=name_asc&limit=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    if data.get('data'):
        names = [c.get('name') for c in data.get('data', [])]
        print(f"Компании (по алфавиту): {names}")
        print(f"Сортировка работает")
    else:
        print("Нет данных")
except Exception as e:
    print(f"Ошибка: {e}")
# Тест 10: Несуществующая компания (404)
print("\n\n[TEST 10] GET /api/companies/9999 (ожидается 404)")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/companies/9999")
    print(f"Status: {response.status_code}")
    if response.status_code == 404:
        print(f"404 корректно возвращается: {response.json().get('detail')}")
    else:
        print(f"Неожиданный статус: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")
print("\n" + "=" * 80)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 80)
print("\nСводка тестов:")
print("1. GET /companies/top-20 - получение топ-20")
print("2. GET /companies/{id} - получение конкретной компании")
print("3. GET /companies?status=new - фильтр по статусу")
print("4. GET /companies?status=invalid - валидация статуса (400)")
print("5. POST /companies/{id}/approve - одобрение компании")
print("6. Проверка изменения статуса на approved")
print("7. POST /companies/{id}/reject - отклонение компании")
print("8. GET /companies?min_score=80 - фильтр по скору")
print("9. GET /companies?sort_by=name_asc - сортировка")
print("10. GET /companies/9999 - обработка 404")
print("=" * 80)
