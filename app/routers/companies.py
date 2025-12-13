"""
Companies Router - Эндпоинты для работы с компаниями
"""

from fastapi import APIRouter, Query


router = APIRouter()


@router.get("/companies/top-20")
async def get_top_companies():
    """
    Получить Top-20 компаний по скору
    """
    return {"status": "not_implemented"}


@router.get("/companies/{id}")
async def get_company_details(id: int):
    """
    Получить детали конкретной компании
    
    Args:
        id: ID компании
    """
    return {"status": "not_implemented"}


@router.post("/companies/{id}/approve")
async def approve_company(id: int):
    """
    Одобрить компанию (статус -> approved)
    
    Args:
        id: ID компании
    """
    return {"status": "not_implemented"}


@router.post("/companies/{id}/reject")
async def reject_company(id: int):
    """
    Отклонить компанию (статус -> rejected)
    
    Args:
        id: ID компании
    """
    return {"status": "not_implemented"}


@router.get("/companies")
async def get_companies(
    status: str | None = Query(None, description="Фильтр по статусу"),
    industry: str | None = Query(None, description="Фильтр по индустрии"),
    min_score: float | None = Query(None, ge=0, le=100, description="Минимальный скор"),
    sort_by: str | None = Query(None, description="Сортировка"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(20, ge=1, le=100, description="Количество записей")
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
    return {"status": "not_implemented"}
