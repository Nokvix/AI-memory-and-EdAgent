from pydantic import BaseModel
from typing import List, Optional


class CompanyResponse(BaseModel):
    id: int
    name: str
    score: float
    vacancy_count: int
    status: str
    main_skills: List[str] = []

    class Config:
        from_attributes = True


class LetterResponse(BaseModel):
    id: int
    subject: str
    body: str
    status: str

    class Config:
        from_attributes = True
