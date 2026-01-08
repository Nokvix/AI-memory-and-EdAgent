"""
Email Service - Отправка писем компаниям (с заглушкой)
"""

from datetime import datetime
from sqlalchemy.orm import Session
import logging

from app.models.models import Letter, Company
from app.schemas.schemas import EmailStatusResponse

# Настройка логирования
logger = logging.getLogger(__name__)


def send_email(
    db: Session,
    company_id: int,
    email: str,
    dry_run: bool = False
) -> EmailStatusResponse:
    """
    Отправить письмо компании по email (с заглушкой отправки)
    
    Args:
        db: SQLAlchemy сессия
        company_id: ID компании
        email: Email адрес получателя
        dry_run: если True, только проверка без реальной отправки
        
    Returns:
        EmailStatusResponse с информацией об отправке
        
    Raises:
        ValueError: если компания не найдена, письмо не найдено или не approved
    """
    # Проверяем существование компании
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise ValueError(f"Компания с ID {company_id} не найдена")
    
    # Получаем последнее письмо компании
    letter = db.query(Letter).filter(
        Letter.company_id == company_id
    ).order_by(Letter.created_at.desc()).first()
    
    if not letter:
        raise ValueError(f"Письмо для компании {company_id} не найдено")
    
    # Проверяем статус письма
    if letter.status != "approved":
        raise ValueError(
            f"Письмо должно быть одобрено перед отправкой. "
            f"Текущий статус: {letter.status}"
        )
    
    # Dry run режим - только логирование
    if dry_run:
        logger.info(f"[DRY RUN] Отправка письма компании {company.name}")
        logger.info(f"[DRY RUN] Email: {email}")
        logger.info(f"[DRY RUN] Тема: {letter.subject}")
        logger.info(f"[DRY RUN] Текст (первые 100 символов): {letter.body[:100]}...")
        
        print(f"\n{'='*80}")
        print(f"🧪 DRY RUN MODE - Отправка письма")
        print(f"{'='*80}")
        print(f"Компания: {company.name}")
        print(f"Email: {email}")
        print(f"Тема: {letter.subject}")
        print(f"Текст (первые 150 символов):\n{letter.body[:150]}...")
        print(f"{'='*80}\n")
        
        return EmailStatusResponse(
            company_id=company_id,
            email=email,
            sent_at=None,
            delivery_status="pending",
            opened_at=None,
            clicked_at=None,
            bounced=False,
            error=None
        )
    
    # Реальная "отправка" (заглушка)
    else:
        logger.info(f"[SEND] Отправка письма компании {company.name}")
        logger.info(f"[SEND] Email: {email}")
        logger.info(f"[SEND] Тема: {letter.subject}")
        
        print(f"\n{'='*80}")
        print(f"📧 ОТПРАВКА ПИСЬМА")
        print(f"{'='*80}")
        print(f"Компания: {company.name}")
        print(f"Email: {email}")
        print(f"Тема: {letter.subject}")
        print(f"Статус: ✅ Отправлено (заглушка)")
        print(f"{'='*80}\n")
        
        # Обновляем статус письма
        letter.status = "sent"
        letter.sent_at = datetime.utcnow()
        db.commit()
        db.refresh(letter)
        
        # Обновляем статус компании
        company.status = "sent"
        db.commit()
        
        return EmailStatusResponse(
            company_id=company_id,
            email=email,
            sent_at=letter.sent_at,
            delivery_status="delivered",  # Заглушка: сразу считаем доставленным
            opened_at=None,
            clicked_at=None,
            bounced=False,
            error=None
        )


def get_email_status(db: Session, company_id: int) -> EmailStatusResponse:
    """
    Получить статус отправки письма компании
    
    Args:
        db: SQLAlchemy сессия
        company_id: ID компании
        
    Returns:
        EmailStatusResponse с информацией о статусе
        
    Raises:
        ValueError: если компания не найдена или письмо не найдено
    """
    # Проверяем существование компании
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise ValueError(f"Компания с ID {company_id} не найдена")
    
    # Получаем последнее письмо компании
    letter = db.query(Letter).filter(
        Letter.company_id == company_id
    ).order_by(Letter.created_at.desc()).first()
    
    if not letter:
        raise ValueError(f"Письмо для компании {company_id} не найдено")
    
    # Определяем delivery_status на основе статуса письма
    if letter.status == "sent":
        delivery_status = "delivered"
    elif letter.status == "approved":
        delivery_status = "pending"
    else:  # draft, rejected
        delivery_status = "pending"
    
    # В реальной системе здесь был бы запрос к email-провайдеру (SendGrid, AWS SES и т.д.)
    # Для заглушки возвращаем базовую информацию
    return EmailStatusResponse(
        company_id=company_id,
        email="unknown@example.com",  # В реальной системе брали бы из БД или tracking
        sent_at=letter.sent_at,
        delivery_status=delivery_status,
        opened_at=None,  # Заглушка: нет tracking
        clicked_at=None,  # Заглушка: нет tracking
        bounced=False,
        error=None
    )
