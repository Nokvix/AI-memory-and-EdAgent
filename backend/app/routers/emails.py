"""
Emails Router - Эндпоинты для отправки писем по email
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import EmailSendRequest, EmailStatusResponse
from app.services import email_service

router = APIRouter()


@router.post("/emails/send/{company_id}", response_model=EmailStatusResponse)
async def send_email_to_company(
    company_id: int,
    request: EmailSendRequest,
    dry_run: bool = Query(False, description="Если true, только проверка без отправки"),
    db: Session = Depends(get_db)
):
    """
    Отправить письмо компании по email (требуется письмо в статусе approved)
    
    Args:
        company_id: ID компании
        request: данные для отправки (email адрес)
        dry_run: если True, только проверяет без реальной отправки
        db: сессия БД
        
    Returns:
        EmailStatusResponse с информацией об отправке
        
    Raises:
        404: если компания или письмо не найдены
        400: если письмо не в статусе approved
    """
    try:
        result = email_service.send_email(
            db=db,
            company_id=company_id,
            email=request.email,
            dry_run=dry_run
        )
        return result
    except ValueError as e:
        error_msg = str(e)
        # Определяем тип ошибки
        if "не найдена" in error_msg or "не найдено" in error_msg:
            raise HTTPException(status_code=404, detail=error_msg)
        else:  # Ошибка валидации статуса
            raise HTTPException(status_code=400, detail=error_msg)


@router.get("/emails/status/{company_id}", response_model=EmailStatusResponse)
async def get_email_status(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить статус отправки письма
    
    Args:
        company_id: ID компании
        db: сессия БД
        
    Returns:
        EmailStatusResponse с информацией о статусе доставки
        
    Raises:
        404: если компания или письмо не найдены
    """
    try:
        result = email_service.get_email_status(db=db, company_id=company_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
