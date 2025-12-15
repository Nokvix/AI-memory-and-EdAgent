"""
Тестовые запросы к Emails API
Сценарий: создание письма → одобрение → dry_run отправка → реальная отправка → проверка статуса
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 80)
print("ТЕСТИРОВАНИЕ EMAILS API - ПОЛНЫЙ СЦЕНАРИЙ")
print("=" * 80)

company_id = 1
test_email = "hr@kontour.ru"

# Шаг 1: Создание письма (draft)
print("\n[STEP 1] POST /api/letters/generate/1?template=formal")
print("-" * 80)
try:
    response = requests.post(f"{BASE_URL}/letters/generate/{company_id}?template=formal")
    print(f"Status: {response.status_code}")
    letter_data = response.json()
    print(f"Letter ID: {letter_data.get('id')}")
    print(f"Status: {letter_data.get('status')}")
    print(f"Subject: {letter_data.get('subject')}")
    letter_id = letter_data.get("id")
except Exception as e:
    print(f"Ошибка: {e}")
    letter_id = None

# Шаг 2: Попытка отправки без одобрения (должна вернуть 400)
print("\n\n[STEP 2] POST /api/emails/send/1 (без одобрения - ожидается ошибка)")
print("-" * 80)
try:
    response = requests.post(
        f"{BASE_URL}/emails/send/{company_id}",
        json={"email": test_email}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print(f"Ожидаемая ошибка: {response.json().get('detail')}")
    else:
        print(f"Неожиданный статус: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")

# Шаг 3: Одобрение письма
if letter_id:
    print(f"\n\n[STEP 3] POST /api/letters/{letter_id}/approve")
    print("-" * 80)
    try:
        response = requests.post(
            f"{BASE_URL}/letters/{letter_id}/approve",
            json={}
        )
        print(f"Status: {response.status_code}")
        approved_data = response.json()
        print(f"Letter Status: {approved_data.get('status')}")
        print(f"Письмо одобрено")
    except Exception as e:
        print(f"Ошибка: {e}")

# Шаг 4: Dry run отправка
print(f"\n\n[STEP 4] POST /api/emails/send/{company_id}?dry_run=true")
print("-" * 80)
try:
    response = requests.post(
        f"{BASE_URL}/emails/send/{company_id}?dry_run=true",
        json={"email": test_email}
    )
    print(f"Status: {response.status_code}")
    email_data = response.json()
    print(json.dumps(email_data, indent=2, ensure_ascii=False))
    print(f"\nDry run выполнен (статус письма не изменён)")
except Exception as e:
    print(f"Ошибка: {e}")

# Шаг 5: Проверка статуса (письмо всё ещё approved, не sent)
print(f"\n\n[STEP 5] GET /api/letters/{company_id} (проверка что статус не изменился)")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/letters/{company_id}")
    print(f"Status: {response.status_code}")
    letter_check = response.json()
    print(f"Letter Status: {letter_check.get('status')}")
    if letter_check.get('status') == 'approved':
        print(f"Статус остался 'approved' после dry run")
    else:
        print(f"Статус изменился: {letter_check.get('status')}")
except Exception as e:
    print(f"Ошибка: {e}")

# Шаг 6: Реальная отправка
print(f"\n\n[STEP 6] POST /api/emails/send/{company_id}?dry_run=false")
print("-" * 80)
try:
    response = requests.post(
        f"{BASE_URL}/emails/send/{company_id}?dry_run=false",
        json={"email": test_email}
    )
    print(f"Status: {response.status_code}")
    sent_data = response.json()
    print(json.dumps(sent_data, indent=2, ensure_ascii=False))
    print(f"\nПисьмо отправлено")
except Exception as e:
    print(f"Ошибка: {e}")

# Шаг 7: Проверка статуса письма после отправки
print(f"\n\n[STEP 7] GET /api/letters/{company_id} (проверка что статус = sent)")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/letters/{company_id}")
    print(f"Status: {response.status_code}")
    final_letter = response.json()
    print(f"Letter Status: {final_letter.get('status')}")
    if final_letter.get('status') == 'sent':
        print(f"Статус изменился на 'sent'")
    else:
        print(f"Статус: {final_letter.get('status')}")
except Exception as e:
    print(f"Ошибка: {e}")
# Шаг 8: Получение статуса отправки email
print(f"\n\n[STEP 8] GET /api/emails/status/{company_id}")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/emails/status/{company_id}")
    print(f"Status: {response.status_code}")
    status_data = response.json()
    print(json.dumps(status_data, indent=2, ensure_ascii=False))
    print(f"\nСтатус получен")
except Exception as e:
    print(f"Ошибка: {e}")

# Шаг 9: Попытка повторной отправки (должна вернуть ошибку)
print(f"\n\n[STEP 9] POST /api/emails/send/{company_id} (повторная отправка - ожидается ошибка)")
print("-" * 80)
try:
    response = requests.post(
        f"{BASE_URL}/emails/send/{company_id}",
        json={"email": test_email}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print(f"Ожидаемая ошибка: {response.json().get('detail')}")
    else:
        print(f"Неожиданный результат: {response.json()}")
except Exception as e:
    print(f"Ошибка: {e}")
print("\n" + "=" * 80)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 80)
print("\nСводка:")
print("1. Создание письма (draft)")
print("2. Защита от отправки без одобрения (400)")
print("3. Одобрение письма (approved)")
print("4. Dry run отправка (без изменения статуса)")
print("5. Проверка неизменности статуса после dry run")
print("6. Реальная отправка (статус → sent)")
print("7. Проверка изменения статуса на sent")
print("8. Получение статуса доставки")
print("9. Защита от повторной отправки (400)")
print("=" * 80)
