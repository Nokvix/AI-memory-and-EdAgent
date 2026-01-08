"""
FastAPI MVP Application - Entry Point
Управление компаниями, письмами и email-рассылками
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import companies, letters, emails


# Создание приложения
app = FastAPI(
    title="AI Memory & EdAgent API",
    description="MVP для управления компаниями и рассылкой писем",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS настройки для MVP (разрешить всё)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров с префиксом /api
app.include_router(companies.router, prefix="/api", tags=["companies"])
app.include_router(letters.router, prefix="/api", tags=["letters"])
app.include_router(emails.router, prefix="/api", tags=["emails"])


# Health check эндпоинт
@app.get("/health", tags=["health"])
async def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "message": "API is running",
        "version": "1.0.0"
    }


@app.get("/", tags=["root"])
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "AI Memory & EdAgent API",
        "docs": "/docs",
        "health": "/health"
    }
