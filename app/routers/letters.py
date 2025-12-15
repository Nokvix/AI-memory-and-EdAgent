"""
Letters Router - Эндпоинты для работы с письмами
"""

from fastapi import APIRouter, Query, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import (
    LetterResponse, 
    LetterApproveRequest, 
    LetterRejectRequest, 
    LetterUpdateRequest,
    PaginatedLettersResponse
)
from app.services import letter_service


router = APIRouter()


@router.get("/letters/{company_id}", response_model=LetterResponse)
async def get_letter_for_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить письмо для компании
    
    Args:
        company_id: ID компании
    """
    letter = letter_service.get_letter_by_company_id(db, company_id)
    
    if not letter:
        raise HTTPException(
            status_code=404,
            detail=f"Письмо для компании {company_id} не найдено"
        )
    
    return LetterResponse(
        id=letter.id,
        subject=letter.subject,
        body=letter.body,
        status=letter.status,
        company_name=letter.company.name if letter.company else None
    )


@router.post("/letters/generate/{company_id}", status_code=201, response_model=LetterResponse)
async def generate_letter(
    company_id: int,
    template: str = Query("formal", description="Тип шаблона: formal или informal"),
    db: Session = Depends(get_db)
):
    """
    Сгенерировать письмо для компании по шаблону
    
    Args:
        company_id: ID компании
        template: formal или informal (по умолчанию formal)
    """
    # Валидация template
    if template not in ["formal", "informal"]:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый тип шаблона: {template}. Разрешены: 'formal', 'informal'"
        )
    
    try:
        letter = letter_service.create_or_replace_draft(db, company_id, template)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return LetterResponse(
        id=letter.id,
        subject=letter.subject,
        body=letter.body,
        status=letter.status,
        company_name=letter.company.name if letter.company else None
    )


@router.post("/letters/{letter_id}/approve", response_model=LetterResponse)
async def approve_letter(
    letter_id: int,
    request: LetterApproveRequest = Body(default=LetterApproveRequest()),
    db: Session = Depends(get_db)
):
    """
    Одобрить письмо (статус -> approved)
    
    Args:
        letter_id: ID письма
        request: опциональный body для замены текста
    """
    try:
        letter = letter_service.approve_letter(db, letter_id, request.body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return LetterResponse(
        id=letter.id,
        subject=letter.subject,
        body=letter.body,
        status=letter.status,
        company_name=letter.company.name if letter.company else None
    )


@router.post("/letters/{letter_id}/reject", response_model=LetterResponse)
async def reject_letter(
    letter_id: int,
    request: LetterRejectRequest = Body(default=LetterRejectRequest()),
    db: Session = Depends(get_db)
):
    """
    Отклонить письмо (статус -> rejected)
    
    Args:
        letter_id: ID письма
        request: опциональная причина отклонения
    """
    try:
        letter = letter_service.reject_letter(db, letter_id, request.reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return LetterResponse(
        id=letter.id,
        subject=letter.subject,
        body=letter.body,
        status=letter.status,
        company_name=letter.company.name if letter.company else None
    )


@router.put("/letters/{letter_id}", response_model=LetterResponse)
async def update_letter(
    letter_id: int,
    request: LetterUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Обновить текст письма (перегенерировать)
    
    Args:
        letter_id: ID письма
        request: новый текст письма (required)
    """
    try:
        letter = letter_service.update_letter(db, letter_id, request.body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return LetterResponse(
        id=letter.id,
        subject=letter.subject,
        body=letter.body,
        status=letter.status,
        company_name=letter.company.name if letter.company else None
    )


@router.get("/letters", response_model=PaginatedLettersResponse)
async def get_letters(
    status: str | None = Query(None, description="Фильтр по статусу"),
    company_id: int | None = Query(None, description="Фильтр по ID компании"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """
    Получить все письма с фильтрацией
    
    Args:
        status: draft, approved, rejected, sent
        company_id: ID компании
        page: номер страницы
        limit: количество записей
    """
    # Валидация status если указан
    if status and status not in ["draft", "approved", "rejected", "sent"]:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый статус: {status}. Разрешены: draft, approved, rejected, sent"
        )
    
    items, total = letter_service.list_letters(db, status, company_id, page, limit)
    
    # Преобразуем в LetterResponse с company_name
    letter_responses = [
        LetterResponse(
            id=letter.id,
            subject=letter.subject,
            body=letter.body,
            status=letter.status,
            company_name=letter.company.name if letter.company else None
        )
        for letter in items
    ]
    
    return PaginatedLettersResponse(
        data=letter_responses,
        total=total,
        page=page,
        limit=limit
    )
