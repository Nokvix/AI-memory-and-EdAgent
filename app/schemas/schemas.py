from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CompanyResponse(BaseModel):
    id: int
    name: str
    url: str
    industry: str
    score: float
    vacancy_count: int
    status: str
    main_skills: List[str] = []

    class Config:
        from_attributes = True


class CompanyApproveRequest(BaseModel):
    """Запрос на одобрение компании"""
    comment: Optional[str] = Field(None, description="Комментарий к одобрению")


class CompanyRejectRequest(BaseModel):
    """Запрос на отклонение компании"""
    reason: Optional[str] = Field(None, description="Причина отклонения")


class PaginatedCompaniesResponse(BaseModel):
    """Пагинированный список компаний"""
    data: List[CompanyResponse] = Field(..., description="Список компаний")
    total: int = Field(..., description="Общее количество компаний")
    page: int = Field(..., description="Текущая страница")
    limit: int = Field(..., description="Количество записей на странице")


class LetterResponse(BaseModel):
    """Базовая схема ответа для письма"""
    id: int
    subject: str
    body: str
    status: str
    company_name: Optional[str] = Field(None, description="Название компании (для списков)")

    class Config:
        from_attributes = True


class LetterGenerateRequest(BaseModel):
    """Запрос на генерацию письма (пустая схема, параметры в query)"""
    pass


class LetterApproveRequest(BaseModel):
    """Запрос на одобрение письма"""
    body: Optional[str] = Field(None, description="Отредактированный текст письма")


class LetterRejectRequest(BaseModel):
    """Запрос на отклонение письма"""
    reason: Optional[str] = Field(None, description="Причина отклонения письма")


class LetterUpdateRequest(BaseModel):
    """Запрос на обновление текста письма"""
    body: str = Field(..., description="Новый текст письма")


class PaginatedLettersResponse(BaseModel):
    """Пагинированный список писем"""
    data: List[LetterResponse] = Field(..., description="Список писем")
    total: int = Field(..., description="Общее количество писем")
    page: int = Field(..., description="Текущая страница")
    limit: int = Field(..., description="Количество записей на странице")


class EmailSendRequest(BaseModel):
    """Запрос на отправку письма по email"""
    email: str = Field(..., description="Email адрес получателя")


class EmailStatusResponse(BaseModel):
    """Статус отправленного email"""
    company_id: int = Field(..., description="ID компании")
    email: str = Field(..., description="Email адрес получателя")
    sent_at: Optional[datetime] = Field(None, description="Время отправки")
    delivery_status: str = Field(..., description="Статус доставки: pending, delivered, failed, bounced")
    opened_at: Optional[datetime] = Field(None, description="Время открытия письма")
    clicked_at: Optional[datetime] = Field(None, description="Время клика по ссылке")
    bounced: bool = Field(default=False, description="Письмо отклонено сервером")
    error: Optional[str] = Field(None, description="Текст ошибки при отправке")

    class Config:
        from_attributes = True
