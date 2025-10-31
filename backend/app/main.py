# Импорт необходимых компонентов FastAPI и зависимостей
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware  # Для CORS (междоменных запросов)
from sqlalchemy.orm import Session  # Для типизации сессии БД
from typing import List  # Для типизации списков

# 📦 ИМПОРТЫ ИЗ ПРОЕКТА
from app import models, schemas, crud  # Модели, схемы и CRUD операции
from app.database import engine, get_db  # Движок БД и генератор сессий

# 🗃️ СОЗДАНИЕ ТАБЛИЦ В БАЗЕ ДАННЫХ
# Автоматически создает все таблицы на основе SQLAlchemy моделей
# В продакшене обычно используются миграции (Alembic)
models.Base.metadata.create_all(bind=engine)

# 🚀 СОЗДАНИЕ FASTAPI ПРИЛОЖЕНИЯ
app = FastAPI(title="User Management API")  # С заголовком для документации

# 🌐 НАСТРОЙКА CORS (CROSS-ORIGIN RESOURCE SHARING)
# Разрешает запросы с фронтенда (React на порту 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Домены фронтенда
    allow_credentials=True,  # Разрешить куки и авторизацию
    allow_methods=["*"],  # Разрешить все HTTP методы (GET, POST, etc.)
    allow_headers=["*"],  # Разрешить все заголовки
)


# 🏠 КОРНЕВОЙ ЭНДПОИНТ - ПРОВЕРКА РАБОТОСПОСОБНОСТИ API
@app.get("/")
def read_root():
    """Возвращает статус работы API"""
    return {"message": "User Management API is running"}


# 👤 СОЗДАНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Создает нового пользователя в системе
    - Валидирует данные через схему UserCreate
    - Проверяет уникальность email
    - Возвращает созданного пользователя
    """
    # Вызываем CRUD операцию для создания пользователя
    db_user = crud.create_user(db=db, user=user)

    # Если пользователь с таким email уже существует
    if db_user is None:
        # Возвращаем ошибку 400 Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Возвращаем созданного пользователя (автоматически конвертируется в JSON)
    return db_user


# 📋 ПОЛУЧЕНИЕ СПИСКА ПОЛЬЗОВАТЕЛЕЙ С ПАГИНАЦИЕЙ
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Возвращает список пользователей с поддержкой пагинации
    - skip: сколько записей пропустить (для постраничного вывода)
    - limit: максимальное количество записей (по умолчанию 100)
    """
    # Получаем пользователей через CRUD с пагинацией
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# 🔍 ПОЛУЧЕНИЕ КОНКРЕТНОГО ПОЛЬЗОВАТЕЛЯ ПО ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Возвращает пользователя по его ID
    - Если пользователь не найден, возвращает 404 ошибку
    """
    # Ищем пользователя в базе данных
    db_user = crud.get_user_by_id(db, user_id=user_id)

    # Если пользователь не найден
    if db_user is None:
        # Возвращаем ошибку 404 Not Found
        raise HTTPException(status_code=404, detail="User not found")

    # Возвращаем найденного пользователя
    return db_user