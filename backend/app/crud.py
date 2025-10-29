from sqlalchemy.orm import Session
from app import models
from app.schemas import UserCreate

# Остальной код без изменений...
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return None

    db_user = models.User(name=user.name, email=user.email, bio=user.bio)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
