from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# 🎯 БАЗОВАЯ СХЕМА ПОЛЬЗОВАТЕЛЯ
# Определяет общие поля для всех схем пользователя
class UserBase(BaseModel):
    name: str                    # Обязательное поле: имя пользователя (строка)
    email: EmailStr              # Обязательное поле: email с автоматической валидацией формата
    bio: Optional[str] = None    # Опциональное поле: биография (может быть None)

# 🆕 СХЕМА ДЛЯ СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ
# Используется при получении данных от клиента (POST /users/)
class UserCreate(UserBase):
    # Наследует все поля от UserBase без изменений
    # name: str (обязательно)
    # email: EmailStr (обязательно)
    # bio: Optional[str] = None (опционально)
    pass

# 👤 СХЕМА ДЛЯ ОТВЕТА API
# Используется при возврате данных клиенту (после создания/чтения пользователя)
class User(UserBase):
    id: int  # Уникальный идентификатор пользователя (генерируется базой данных)

    # ⚙️ КОНФИГУРАЦИЯ PYDANTIC v2
    # from_attributes=True позволяет создавать Pydantic модели из ORM объектов (ранее orm_mode = True)
    # Это позволяет автоматически конвертировать SQLAlchemy модели в Pydantic схемы
    model_config = ConfigDict(from_attributes=True)