# Импорт необходимых библиотек
from sqlalchemy import create_engine  # Для создания подключения к БД
from sqlalchemy.orm import sessionmaker  # Для создания сессий работы с БД
from sqlalchemy.orm import declarative_base  # Для создания базового класса моделей
import os  # Для работы с переменными окружения
from dotenv import load_dotenv  # Для загрузки переменных из .env файла

# 📁 ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# Загружает переменные из файла .env в текущее окружение
load_dotenv()

# 🔗 ФОРМИРОВАНИЕ URL ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ
# Формат: postgresql://username:password@host:port/database_name
# Все данные берутся из переменных окружения для безопасности
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# 🚀 СОЗДАНИЕ ДВИЖКА БАЗЫ ДАННЫХ
# Движок - это основной интерфейс к базе данных, управляет подключениями
engine = create_engine(DATABASE_URL)

# 🎯 СОЗДАНИЕ ФАБРИКИ СЕССИЙ
# SessionLocal - это фабрика для создания сессий работы с БД
SessionLocal = sessionmaker(
    autocommit=False,  # Автоматически не коммитить изменения (ручное управление)
    autoflush=False,   # Автоматически не сбрасывать сессию (лучшая производительность)
    bind=engine        # Привязываем к созданному движку
)

# 🏗️ СОЗДАНИЕ БАЗОВОГО КЛАССА ДЛЯ МОДЕЛЕЙ
# Все модели SQLAlchemy будут наследоваться от этого класса
Base = declarative_base()

# 🔄 ГЕНЕРАТОР СЕССИЙ ДЛЯ FASTAPI DEPENDENCIES
def get_db():
    """
    Генератор сессий базы данных для использования в FastAPI зависимостях
    Гарантирует закрытие сессии после завершения запроса
    """
    # Создаем новую сессию для каждого запроса
    db = SessionLocal()
    try:
        # Отдаем сессию в обработчик запроса
        yield db
    finally:
        # Всегда закрываем сессию после завершения работы (даже при ошибках)
        db.close()