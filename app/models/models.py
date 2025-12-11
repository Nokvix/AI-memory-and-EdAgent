from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String)
    industry = Column(String, nullable=True)
    score = Column(Float, default=0.0)
    vacancy_count = Column(Integer, default=0)
    main_skills = Column(JSON, default=[])
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vacancies = relationship("Vacancy", back_populates="company")
    letters = relationship("Letter", back_populates="company")
    logs = relationship("ApprovalLog", back_populates="company")

class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    position = Column(String)
    skills = Column(JSON)
    url = Column(String)

    company = relationship("Company", back_populates="vacancies")


class Letter(Base):
    __tablename__ = "letters"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    template = Column(String)
    subject = Column(String)
    body = Column(Text)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)

    company = relationship("Company", back_populates="letters")


class ApprovalLog(Base):
    __tablename__ = "approval_log"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    action = Column(String)
    details = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="logs")