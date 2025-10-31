from sqlalchemy.orm import Session
from app import models
from app.schemas import UserCreate


def get_user_by_email(db: Session, email: str):
    """
    🔍 Поиск пользователя по email в базе данных
    Возвращает пользователя или None если не найден
    """
    # Создаем SQL запрос: SELECT * FROM users WHERE email = ?
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """
    🔍 Поиск пользователя по ID в базе данных
    Возвращает пользователя или None если не найден
    """
    # Создаем SQL запрос: SELECT * FROM users WHERE id = ?
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    """
    🆕 Создание нового пользователя в базе данных
    Возвращает созданного пользователя или None если email уже существует
    """
    # Проверяем нет ли пользователя с таким email
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return None  # Пользователь с таким email уже существует

    # Создаем новый объект пользователя из данных схемы
    db_user = models.User(
        name=user.name,  # Имя пользователя
        email=user.email,  # Email пользователя
        bio=user.bio  # Биография (может быть None)
    )

    # Добавляем пользователя в сессию (подготовка к сохранению)
    db.add(db_user)

    # Сохраняем изменения в базе данных (выполняем INSERT)
    db.commit()

    # Обновляем объект из базы данных (получаем сгенерированный ID)
    db.refresh(db_user)

    return db_user  # Возвращаем созданного пользователя


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    📋 Получение списка пользователей с пагинацией
    skip - сколько записей пропустить (для пагинации)
    limit - максимальное количество записей для возврата
    """
    # Создаем SQL запрос: SELECT * FROM users OFFSET ? LIMIT ?
    return db.query(models.User).offset(skip).limit(limit).all()