"""
Тестовые запросы к Letters API
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 80)
print("ТЕСТИРОВАНИЕ LETTERS API")
print("=" * 80)

# Тест 1: Генерация письма
print("\n[1] POST /api/letters/generate/1?template=formal")
print("-" * 80)
try:
    response = requests.post(f"{BASE_URL}/letters/generate/1?template=formal")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    letter_id = data.get("id")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    letter_id = None

# Тест 2: Получить письмо компании
print("\n\n[2] GET /api/letters/1")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/letters/1")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Тест 3: Одобрить письмо
if letter_id:
    print(f"\n\n[3] POST /api/letters/{letter_id}/approve")
    print("-" * 80)
    try:
        response = requests.post(
            f"{BASE_URL}/letters/{letter_id}/approve",
            json={"body": None}
        )
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# Тест 4: Список писем
print("\n\n[4] GET /api/letters?status=approved&page=1&limit=10")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/letters?status=approved&page=1&limit=10")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Тест 5: Отклонить письмо (создадим новое)
print("\n\n[5] Создание и отклонение нового письма")
print("-" * 80)
try:
    # Создаём новое письмо
    response = requests.post(f"{BASE_URL}/letters/generate/1?template=informal")
    new_letter_id = response.json().get("id")
    print(f"Создано письмо ID: {new_letter_id}")
    
    # Отклоняем его
    response = requests.post(
        f"{BASE_URL}/letters/{new_letter_id}/reject",
        json={"reason": "Тестовое отклонение"}
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n" + "=" * 80)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 80)
