# Backend API - User Management

FastAPI-based backend service for user management with PostgreSQL database.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Environment variables configured

### Installation
```bash
# Clone repository
git clone <repository-url>
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials



DB_USER=ваш_username
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ваша_база_данных



uvicorn app.main:app --reload
API будет доступно по адресу: http://localhost:8000

Структура проекта:
backend/
├── app/
│   ├── main.py              # FastAPI приложение и маршруты
│   ├── database.py          # Конфигурация БД
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   └── crud.py              # Операции с БД
└── .env


Модели (models.py)

    User - модель пользователя с полями: id, name, email, bio

Схемы (schemas.py)

    UserCreate - для создания пользователя

    User - для ответов API

CRUD операции (crud.py)

    create_user() - создание пользователя с проверкой email

    get_user_by_id() - поиск пользователя по ID

    get_users() - получение списка пользователей


