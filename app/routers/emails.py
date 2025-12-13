"""
Emails Router - Эндпоинты для отправки писем по email
"""

from fastapi import APIRouter, Query


router = APIRouter()


@router.post("/emails/send/{company_id}")
async def send_email_to_company(
    company_id: int,
    dry_run: bool = Query(False, description="Если true, только проверка без отправки")
):
    """
    Отправить письмо компании по email (требуется письмо в статусе approved)
    
    Args:
        company_id: ID компании
        dry_run: если True, только проверяет без реальной отправки
    """
    return {"status": "not_implemented"}


@router.get("/emails/status/{company_id}")
async def get_email_status(company_id: int):
    """
    Получить статус отправки письма
    
    Args:
        company_id: ID компании
    """
    return {"status": "not_implemented"}
