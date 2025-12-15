from app.core.database import engine, Base
from app.models.models import Company

print("Создаем таблицы...")
Base.metadata.create_all(bind=engine)
print("Успех! Файл mvp.db должен появиться.")