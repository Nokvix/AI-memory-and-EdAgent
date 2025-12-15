"""
Companies Router - Эндпоинты для работы с компаниями
"""

from fastapi import APIRouter, Query, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.models.models import Company
from app.schemas.schemas import (
    CompanyResponse,
    CompanyApproveRequest,
    CompanyRejectRequest,
    PaginatedCompaniesResponse
)
# from test_companies_api import company

# Настройка логирования
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/companies/top-20", response_model=List[CompanyResponse])
async def get_top_companies(db: Session = Depends(get_db)):
    """
    Получить Top-20 компаний по скору
    """
    companies = db.query(Company).order_by(Company.score.desc()).limit(20).all()
    
    return [
        CompanyResponse(
            id=company.id,
            name=company.name,
            url=company.url,
            industry=company.industry,
            score=company.score,
            vacancy_count=company.vacancy_count,
            status=company.status,
            main_skills=company.main_skills if company.main_skills else []
        )
        for company in companies
    ]


@router.get("/companies/{id}", response_model=CompanyResponse)
async def get_company_details(id: int, db: Session = Depends(get_db)):
    """
    Получить детали конкретной компании
    
    Args:
        id: ID компании
    """
    company = db.query(Company).filter(Company.id == id).first()
    
    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Компания с ID {id} не найдена"
        )
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        url=company.url,
        industry=company.industry,
        score=company.score,
        vacancy_count=company.vacancy_count,
        status=company.status,
        main_skills=company.main_skills if company.main_skills else []
    )


@router.post("/companies/{id}/approve", response_model=CompanyResponse)
async def approve_company(
    id: int,
    request: CompanyApproveRequest = Body(default=CompanyApproveRequest()),
    db: Session = Depends(get_db)
):
    """
    Одобрить компанию (статус -> approved)
    
    Args:
        id: ID компании
        request: комментарий к одобрению (опционально)
    """
    company = db.query(Company).filter(Company.id == id).first()
    
    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Компания с ID {id} не найдена"
        )
    
    # Обновляем статус
    company.status = "approved"
    db.commit()
    db.refresh(company)
    
    # Логирование действия (вместо ApprovalLog)
    logger.info(f"Company {id} ({company.name}) approved. Comment: {request.comment}")
    print(f"✅ Компания '{company.name}' одобрена. Комментарий: {request.comment or 'Нет'}")
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        score=company.score,
        vacancy_count=company.vacancy_count,
        status=company.status,
        main_skills=company.main_skills if company.main_skills else []
    )


@router.post("/companies/{id}/reject", response_model=CompanyResponse)
async def reject_company(
    id: int,
    request: CompanyRejectRequest = Body(default=CompanyRejectRequest()),
    db: Session = Depends(get_db)
):
    """
    Отклонить компанию (статус -> rejected)
    
    Args:
        id: ID компании
        request: причина отклонения (опционально)
    """
    company = db.query(Company).filter(Company.id == id).first()
    
    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Компания с ID {id} не найдена"
        )
    
    # Обновляем статус
    company.status = "rejected"
    db.commit()
    db.refresh(company)
    
    # Логирование действия (вместо ApprovalLog)
    logger.info(f"Company {id} ({company.name}) rejected. Reason: {request.reason}")
    print(f"Компания '{company.name}' отклонена. Причина: {request.reason or 'Не указана'}")
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        score=company.score,
        vacancy_count=company.vacancy_count,
        status=company.status,
        main_skills=company.main_skills if company.main_skills else []
    )


@router.get("/companies", response_model=PaginatedCompaniesResponse)
async def get_companies(
    status: str | None = Query(None, description="Фильтр по статусу"),
    industry: str | None = Query(None, description="Фильтр по индустрии"),
    min_score: float | None = Query(None, ge=0, le=100, description="Минимальный скор"),
    sort_by: str | None = Query(None, description="Сортировка"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """
    Получить все компании с фильтрацией и пагинацией
    
    Args:
        status: new, approved, rejected, sent, responded
        industry: IT, Finance, etc.
        min_score: 0-100
        sort_by: score_desc, score_asc, name_asc, name_desc
        page: номер страницы
        limit: количество записей
    """
    # Валидация status
    if status and status not in ["new", "approved", "rejected", "sent", "responded"]:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый статус: {status}. Разрешены: new, approved, rejected, sent, responded"
        )
    
    # Базовый запрос
    query = db.query(Company)
    
    # Применяем фильтры
    if status:
        query = query.filter(Company.status == status)
    if industry:
        query = query.filter(Company.industry == industry)
    if min_score is not None:
        query = query.filter(Company.score >= min_score)
    
    # Применяем сортировку
    if sort_by == "score_desc":
        query = query.order_by(Company.score.desc())
    elif sort_by == "score_asc":
        query = query.order_by(Company.score.asc())
    elif sort_by == "name_asc":
        query = query.order_by(Company.name.asc())
    elif sort_by == "name_desc":
        query = query.order_by(Company.name.desc())
    else:
        # Сортировка по умолчанию: по score desc
        query = query.order_by(Company.score.desc())
    
    # Получаем общее количество
    total = query.count()
    
    # Применяем пагинацию
    offset = (page - 1) * limit
    companies = query.offset(offset).limit(limit).all()
    
    # Формируем ответ
    company_responses = [
        CompanyResponse(
            id=company.id,
            name=company.name,
            url=company.url,
            industry=company.industry,
            score=company.score,
            vacancy_count=company.vacancy_count,
            status=company.status,
            main_skills=company.main_skills if company.main_skills else []
        )
        for company in companies
    ]
    
    return PaginatedCompaniesResponse(
        data=company_responses,
        total=total,
        page=page,
        limit=limit
    )
