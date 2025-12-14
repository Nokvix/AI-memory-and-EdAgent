"""
Letter Service - Генерация писем по шаблонам
Pure-функции без зависимостей от БД/ORM
"""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


# Путь к директории с шаблонами
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

# Инициализация Jinja2 окружения
jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    trim_blocks=True,
    lstrip_blocks=True
)


def render_template(template_filename: str, context: dict) -> str:
    """
    Отрендерить Jinja2 шаблон с контекстом
    
    Args:
        template_filename: имя файла шаблона (например, "formal_letter.txt")
        context: словарь с переменными для подстановки
        
    Returns:
        Отрендеренный текст
        
    Raises:
        TemplateNotFound: если шаблон не найден
    """
    try:
        template = jinja_env.get_template(template_filename)
        return template.render(**context)
    except TemplateNotFound:
        raise TemplateNotFound(f"Шаблон {template_filename} не найден в {TEMPLATES_DIR}")


def generate_letter(
    company_name: str,
    skills: list[str],
    template: str = "formal",
    contact_email: str = "procompetencies@urfu.ru",
    university_name: str = "Уральский федеральный университет (УрФУ)"
) -> dict:
    """
    Сгенерировать письмо компании по шаблону
    
    Args:
        company_name: название компании
        skills: список ключевых навыков компании
        template: тип шаблона ("formal" или "informal")
        contact_email: email для связи
        university_name: название университета
        
    Returns:
        Словарь с полями:
        - subject: тема письма
        - body: текст письма
        - template: использованный шаблон
        
    Raises:
        ValueError: если template не "formal" и не "informal"
    """
    # Валидация шаблона
    if template not in ["formal", "informal"]:
        raise ValueError(f"Недопустимый тип шаблона: {template}. Разрешены: 'formal', 'informal'")
    
    # Определение имени файла шаблона
    template_filename = f"{template}_letter.txt"
    
    # Контекст для рендеринга
    context = {
        "company_name": company_name,
        "skills": skills,
        "contact_email": contact_email,
        "university_name": university_name
    }
    
    # Генерация темы письма
    if template == "formal":
        subject = f"Партнёрство с {company_name} — предложение от {university_name}"
    else:  # informal
        subject = f"Сотрудничество с {company_name} и ПроКомпетенциями УрФУ 🚀"
    
    # Рендеринг тела письма
    body = render_template(template_filename, context)
    
    return {
        "subject": subject,
        "body": body,
        "template": template
    }
