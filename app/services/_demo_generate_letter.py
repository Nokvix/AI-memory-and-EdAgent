"""
Демо-скрипт для проверки генерации писем
Запуск: python app/services/_demo_generate_letter.py
"""

from letter_service import generate_letter


def main():
    print("=" * 80)
    print("ДЕМОНСТРАЦИЯ ГЕНЕРАЦИИ ПИСЕМ")
    print("=" * 80)
    print()
    
    # Мок-данные для тестирования
    test_companies = [
        {
            "name": "ООО Контур",
            "skills": ["Python", "Django", "PostgreSQL", "Docker", "REST API"],
            "template": "formal"
        },
        {
            "name": "OZON",
            "skills": ["Java", "Kubernetes", "Microservices", "AWS"],
            "template": "informal"
        }
    ]
    
    # Генерация и вывод писем
    for idx, company_data in enumerate(test_companies, 1):
        print(f"\n{'─' * 80}")
        print(f"ПИСЬМО #{idx}: {company_data['name']} (шаблон: {company_data['template']})")
        print('─' * 80)
        
        try:
            # Генерация письма
            letter = generate_letter(
                company_name=company_data["name"],
                skills=company_data["skills"],
                template=company_data["template"]
            )
            
            # Вывод результата
            print(f"\nТЕМА:")
            print(f"   {letter['subject']}")
            print(f"\nТЕКСТ ПИСЬМА:")
            print("─" * 80)
            print(letter['body'])
            print("─" * 80)
            print(f"\nШаблон: {letter['template']}")
            
        except Exception as e:
            print(f"\nОШИБКА: {e}")
    
    # Тест с невалидным шаблоном
    print(f"\n\n{'=' * 80}")
    print("ТЕСТ ВАЛИДАЦИИ: невалидный шаблон")
    print("=" * 80)
    try:
        generate_letter(
            company_name="Test Company",
            skills=["Python"],
            template="invalid_template"
        )
        print("Ошибка не была выброшена!")
    except ValueError as e:
        print(f"Валидация сработала корректно: {e}")
    
    print(f"\n{'=' * 80}")
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 80)


if __name__ == "__main__":
    main()
