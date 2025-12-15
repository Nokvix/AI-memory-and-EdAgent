"""
Letter Service - Генерация писем по шаблонам и CRUD операции
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from sqlalchemy.orm import Session

from app.models.models import Letter, Company


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
    Сгенерировать письмо компании по шаблону (pure-функция)
    
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


def create_or_replace_draft(db: Session, company_id: int, template: str = "formal") -> Letter:
    """
    Создать новое письмо-черновик или заменить существующий черновик для компании
    
    Args:
        db: SQLAlchemy сессия
        company_id: ID компании
        template: тип шаблона ("formal" или "informal")
        
    Returns:
        Созданное или обновлённое письмо
        
    Raises:
        ValueError: если компания не найдена или template невалиден
    """
    # Проверяем существование компании
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise ValueError(f"Компания с ID {company_id} не найдена")
    
    # Получаем навыки из компании (main_skills - это JSON/list)
    skills = company.main_skills if company.main_skills else []
    
    # Генерируем содержимое письма через существующую pure-функцию
    letter_content = generate_letter(
        company_name=company.name,
        skills=skills,
        template=template
    )
    
    # Ищем существующий черновик для этой компании
    existing_draft = db.query(Letter).filter(
        Letter.company_id == company_id,
        Letter.status == "draft"
    ).first()
    
    if existing_draft:
        # Обновляем существующий черновик
        existing_draft.template = template
        existing_draft.subject = letter_content["subject"]
        existing_draft.body = letter_content["body"]
        existing_draft.created_at = datetime.utcnow()  # Обновляем время
        db.commit()
        db.refresh(existing_draft)
        return existing_draft
    else:
        # Создаём новое письмо
        new_letter = Letter(
            company_id=company_id,
            template=template,
            subject=letter_content["subject"],
            body=letter_content["body"],
            status="draft"
        )
        db.add(new_letter)
        db.commit()
        db.refresh(new_letter)
        return new_letter


def get_letter_by_company_id(db: Session, company_id: int) -> Optional[Letter]:
    """
    Получить письмо для компании (любое, приоритет - последнее созданное)
    
    Args:
        db: SQLAlchemy сессия
        company_id: ID компании
        
    Returns:
        Письмо или None если не найдено
    """
    return db.query(Letter).filter(
        Letter.company_id == company_id
    ).order_by(Letter.created_at.desc()).first()


def approve_letter(db: Session, letter_id: int, body: Optional[str] = None) -> Letter:
    """
    Одобрить письмо (статус -> approved)
    
    Args:
        db: SQLAlchemy сессия
        letter_id: ID письма
        body: опциональный новый текст письма
        
    Returns:
        Обновлённое письмо
        
    Raises:
        ValueError: если письмо не найдено
    """
    letter = db.query(Letter).filter(Letter.id == letter_id).first()
    if not letter:
        raise ValueError(f"Письмо с ID {letter_id} не найдено")
    
    # Обновляем body если передан
    if body:
        letter.body = body
    
    # Меняем статус на approved
    letter.status = "approved"
    letter.approved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(letter)
    return letter


def reject_letter(db: Session, letter_id: int, reason: Optional[str] = None) -> Letter:
    """
    Отклонить письмо (статус -> rejected)
    
    Args:
        db: SQLAlchemy сессия
        letter_id: ID письма
        reason: причина отклонения
        
    Returns:
        Обновлённое письмо
        
    Raises:
        ValueError: если письмо не найдено
    """
    letter = db.query(Letter).filter(Letter.id == letter_id).first()
    if not letter:
        raise ValueError(f"Письмо с ID {letter_id} не найдено")
    
    # Меняем статус на rejected
    letter.status = "rejected"
    letter.rejected_at = datetime.utcnow()
    letter.rejection_reason = reason
    
    db.commit()
    db.refresh(letter)
    return letter


def update_letter(db: Session, letter_id: int, body: str) -> Letter:
    """
    Обновить текст письма (статус сбрасывается в draft)
    
    Args:
        db: SQLAlchemy сессия
        letter_id: ID письма
        body: новый текст письма
        
    Returns:
        Обновлённое письмо
        
    Raises:
        ValueError: если письмо не найдено
    """
    letter = db.query(Letter).filter(Letter.id == letter_id).first()
    if not letter:
        raise ValueError(f"Письмо с ID {letter_id} не найдено")
    
    # Обновляем body и сбрасываем статус в draft
    letter.body = body
    letter.status = "draft"
    letter.approved_at = None
    letter.rejected_at = None
    letter.rejection_reason = None
    
    db.commit()
    db.refresh(letter)
    return letter


def list_letters(
    db: Session,
    status: Optional[str] = None,
    company_id: Optional[int] = None,
    page: int = 1,
    limit: int = 20
) -> tuple[list[Letter], int]:
    """
    Получить список писем с фильтрацией и пагинацией
    
    Args:
        db: SQLAlchemy сессия
        status: фильтр по статусу (draft, approved, rejected, sent)
        company_id: фильтр по ID компании
        page: номер страницы (начиная с 1)
        limit: количество записей на странице
        
    Returns:
        Кортеж (список писем, общее количество)
    """
    # Базовый запрос
    query = db.query(Letter)
    
    # Применяем фильтры
    if status:
        query = query.filter(Letter.status == status)
    if company_id:
        query = query.filter(Letter.company_id == company_id)
    
    # Получаем общее количество
    total = query.count()
    
    # Применяем пагинацию
    offset = (page - 1) * limit
    items = query.order_by(Letter.created_at.desc()).offset(offset).limit(limit).all()
    
    return items, total
