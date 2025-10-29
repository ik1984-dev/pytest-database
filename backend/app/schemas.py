from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    # ИСПРАВЛЕННАЯ КОНФИГУРАЦИЯ для Pydantic v2
    model_config = ConfigDict(from_attributes=True)
