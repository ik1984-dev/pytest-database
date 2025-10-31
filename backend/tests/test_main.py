
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, get_db
from app.models import Base
from app.schemas import UserCreate

# 🧪 НАСТРОЙКА ТЕСТОВОЙ БАЗЫ ДАННЫХ
# SQLite in-memory база - создается в оперативной памяти, исчезает после тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Создание движка БД для тестов
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Разрешаем использование в разных потоках
    poolclass=StaticPool,  # Простой пул соединений для тестов (не для продакшена)
)

# Фабрика сессий для тестовой БД
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 🎯 ФИКСТУРЫ PYTEST
# Фикстура - специальная функция, которая подготавливает данные для тестов
# scope="function" - фикстура пересоздается для каждого теста

@pytest.fixture(scope="function")
def db_session():
    """
    Фикстура: создает и очищает тестовую БД для каждого теста
    - Создает таблицы перед тестом
    - Удаляет таблицы после теста
    - Обеспечивает изоляцию тестов
    """
    print("🔄 Создание тестовой БД...")

    # Создаем все таблицы в БД перед тестом
    Base.metadata.create_all(bind=engine)

    # Создаем сессию для работы с БД
    session = TestingSessionLocal()

    try:
        # yield разделяет код на "до теста" и "после теста"
        # Здесь выполняется сам тест
        yield session
    finally:
        # Очистка после теста (выполняется даже если тест упал)
        session.close()
        Base.metadata.drop_all(bind=engine)  # Удаляем таблицы после теста
        print("🔄 Очистка тестовой БД...")


@pytest.fixture(scope="function")
def client(db_session):
    """
    Фикстура: создает тестового клиента FastAPI с подменой зависимостей
    - Заменяет реальную БД на тестовую
    - Создает тестовый клиент для HTTP запросов
    - Очищает подмены после теста
    """

    def override_get_db():
        """Функция для подмены реальной БД на тестовую"""
        try:
            yield db_session
        finally:
            pass

    # 🔄 ПОДМЕНА ЗАВИСИМОСТЕЙ
    # Заменяем реальное подключение к БД на тестовое
    app.dependency_overrides[get_db] = override_get_db

    # Создаем тестовый клиент - специальный клиент для тестирования FastAPI
    client = TestClient(app)

    # Отдаем клиент тесту
    yield client

    # Очищаем подмены зависимостей после теста
    app.dependency_overrides.clear()


# 🧪 ТЕСТЫ ДЛЯ API УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ
class TestUserManagementAPI:
    """📋 Тесты для API управления пользователями"""

    def test_root_endpoint(self, client):
        """✅ Проверяет, что корневой эндпоинт возвращает правильное сообщение"""
        print("🧪 Тест: Корневой эндпоинт")

        # Отправляем GET запрос на корневой эндпоинт
        response = client.get("/")

        # Проверяем статус код (200 OK - успешный запрос)
        assert response.status_code == 200, "Код статуса должен быть 200"

        # Проверяем структуру ответа
        assert "message" in response.json(), "Ответ должен содержать поле 'message'"
        assert "User Management API is running" in response.json()["message"]

        print("✅ Корневой эндпоинт работает корректно")

    def test_create_user_success(self, client, db_session):
        """✅ Проверяет успешное создание пользователя со всеми полями"""
        print("🧪 Тест: Создание пользователя (успешный сценарий)")

        user_data = {
            "name": "Иван Иванов",
            "email": "ivan@example.com",
            "bio": "Разработчик из Москвы"
        }

        # Отправляем POST запрос для создания пользователя
        response = client.post("/users/", json=user_data)

        # 201 Created - успешное создание ресурса
        assert response.status_code == 201, "Код статуса должен быть 201 (Created)"

        data = response.json()

        # Проверяем все поля ответа
        assert data["name"] == user_data["name"], "Имя должно совпадать"
        assert data["email"] == user_data["email"], "Email должен совпадать"
        assert data["bio"] == user_data["bio"], "Биография должна совпадать"
        assert "id" in data, "Ответ должен содержать ID пользователя"
        assert isinstance(data["id"], int), "ID должен быть целым числом"

        print(f"✅ Пользователь создан: ID={data['id']}, Email={data['email']}")

    def test_create_user_minimal_data(self, client, db_session):
        """✅ Проверяет создание пользователя только с обязательными полями"""
        print("🧪 Тест: Создание пользователя (минимальные данные)")

        user_data = {
            "name": "Анна Петрова",
            "email": "anna@example.com"
            # bio отсутствует - должно работать (опциональное поле)
        }

        response = client.post("/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()

        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["bio"] is None, "Bio должен быть None если не указан"

        print("✅ Пользователь с минимальными данными создан успешно")

    def test_create_user_duplicate_email(self, client, db_session):
        """❌ Проверяет обработку дублирующихся email"""
        print("🧪 Тест: Попытка создания пользователя с дублирующимся email")

        user_data = {
            "name": "Петр Сидоров",
            "email": "petr@example.com",
            "bio": "Первый пользователь"
        }

        # Первый запрос - должен быть успешным
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == 201
        print(f"✅ Первый пользователь создан: {response1.json()['email']}")

        # Второй запрос с тем же email - должен вернуть ошибку
        response2 = client.post("/users/", json=user_data)

        # 400 Bad Request - некорректный запрос (дубликат email)
        assert response2.status_code == 400, "Должна быть ошибка 400"
        assert "detail" in response2.json(), "Ответ должен содержать поле 'detail'"
        assert "already registered" in response2.json()["detail"].lower()

        print("✅ Дублирующий email корректно отклонен")

    def test_create_user_invalid_email(self, client, db_session):
        """❌ Проверяет валидацию некорректного email"""
        print("🧪 Тест: Валидация некорректного email")

        user_data = {
            "name": "Тест User",
            "email": "invalid-email-format",  # Некорректный формат email
            "bio": "Тестовая биография"
        }

        response = client.post("/users/", json=user_data)

        # 422 Unprocessable Entity - ошибка валидации данных
        assert response.status_code == 422, "Должна быть ошибка валидации 422"
        print("✅ Некорректный email корректно отклонен")

    def test_create_user_missing_required_fields(self, client, db_session):
        """❌ Проверяет обработку отсутствия обязательных полей"""
        print("🧪 Тест: Проверка обязательных полей")

        # Тест без имени (обязательное поле)
        user_data_no_name = {
            "email": "noname@example.com",
            "bio": "Без имени"
        }
        response = client.post("/users/", json=user_data_no_name)
        assert response.status_code == 422, "Должна быть ошибка без имени"
        print("✅ Отсутствие имени корректно обнаружено")

        # Тест без email (обязательное поле)
        user_data_no_email = {
            "name": "Без Email",
            "bio": "Без email"
        }
        response = client.post("/users/", json=user_data_no_email)
        assert response.status_code == 422, "Должна быть ошибка без email"
        print("✅ Отсутствие email корректно обнаружено")

    def test_get_users_empty_list(self, client, db_session):
        """✅ Проверяет получение пустого списка пользователей"""
        print("🧪 Тест: Получение пустого списка пользователей")

        response = client.get("/users/")

        assert response.status_code == 200
        assert response.json() == [], "Список должен быть пустым"
        print("✅ Пустой список пользователей возвращен корректно")

    def test_get_users_with_data(self, client, db_session):
        """✅ Проверяет получение списка пользователей с данными"""
        print("🧪 Тест: Получение списка пользователей")

        # Создаем тестовых пользователей
        test_users = [
            {"name": "User One", "email": "user1@example.com", "bio": "Bio 1"},
            {"name": "User Two", "email": "user2@example.com", "bio": "Bio 2"},
            {"name": "User Three", "email": "user3@example.com", "bio": "Bio 3"},
        ]

        created_users = []
        for user_data in test_users:
            response = client.post("/users/", json=user_data)
            assert response.status_code == 201
            created_users.append(response.json())

        print(f"✅ Создано {len(created_users)} тестовых пользователей")

        # Получаем всех пользователей
        response = client.get("/users/")
        assert response.status_code == 200
        users = response.json()

        assert len(users) == len(test_users), "Количество пользователей должно совпадать"

        # Проверяем структуру каждого пользователя
        for user in users:
            assert "id" in user
            assert "name" in user
            assert "email" in user
            assert "bio" in user

        print(f"✅ Получен список из {len(users)} пользователей")

    def test_get_users_pagination(self, client, db_session):
        """✅ Проверяет пагинацию при получении пользователей"""
        print("🧪 Тест: Пагинация списка пользователей")

        # Создаем 5 пользователей
        for i in range(5):
            user_data = {
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "bio": f"Bio {i}"
            }
            client.post("/users/", json=user_data)

        # 📊 ТЕСТИРУЕМ ПАГИНАЦИЮ
        # skip=1 - пропустить первого пользователя
        # limit=2 - вернуть только 2 пользователя
        response = client.get("/users/?skip=1&limit=2")
        assert response.status_code == 200
        users = response.json()

        assert len(users) == 2, "Должно вернуться 2 пользователя"
        assert users[0]["name"] == "User 1"
        assert users[1]["name"] == "User 2"

        print("✅ Пагинация работает корректно")

    def test_get_user_by_id_success(self, client, db_session):
        """✅ Проверяет получение пользователя по ID"""
        print("🧪 Тест: Получение пользователя по ID")

        # Создаем пользователя
        user_data = {
            "name": "Алексей Козлов",
            "email": "alexey@example.com",
            "bio": "Тестовый пользователь для поиска по ID"
        }

        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        print(f"✅ Создан пользователь с ID: {user_id}")

        # Получаем пользователя по ID
        response = client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == user_id
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["bio"] == user_data["bio"]

        print(f"✅ Пользователь с ID {user_id} найден корректно")

    def test_get_user_by_id_not_found(self, client, db_session):
        """❌ Проверяет обработку запроса несуществующего пользователя"""
        print("🧪 Тест: Поиск несуществующего пользователя")

        # Пытаемся найти пользователя с несуществующим ID
        response = client.get("/users/99999")

        # 404 Not Found - ресурс не найден
        assert response.status_code == 404
        assert "detail" in response.json()
        assert "not found" in response.json()["detail"].lower()

        print("✅ Несуществующий пользователь корректно обработан")

    def test_user_data_types(self, client, db_session):
        """✅ Проверяет корректность типов данных в ответах"""
        print("🧪 Тест: Проверка типов данных")

        user_data = {
            "name": "Type Test User",
            "email": "types@example.com",
            "bio": "Testing data types"
        }

        response = client.post("/users/", json=user_data)
        data = response.json()

        # Проверяем типы данных
        assert isinstance(data["id"], int), "ID должен быть integer"
        assert isinstance(data["name"], str), "Name должен быть string"
        assert isinstance(data["email"], str), "Email должен быть string"
        assert isinstance(data["bio"], str), "Bio должен быть string"

        print("✅ Все типы данных корректны")


# 🔧 ТЕСТЫ ДЛЯ НИЗКОУРОВНЕВЫХ CRUD ОПЕРАЦИЙ
class TestCRUDOperations:
    """🔧 Тесты для низкоуровневых CRUD операций"""

    def test_crud_create_and_retrieve(self, db_session):
        """✅ Проверяет создание и получение пользователя через CRUD"""
        print("🧪 Тест: CRUD операции - создание и поиск")

        from app.crud import create_user, get_user_by_email, get_user_by_id
        from app.schemas import UserCreate

        user_data = UserCreate(
            name="CRUD Test User",
            email="crud@example.com",
            bio="Testing CRUD operations"
        )

        # Создаем пользователя через CRUD
        created_user = create_user(db_session, user_data)
        assert created_user is not None
        assert created_user.id is not None
        print(f"✅ CRUD: Пользователь создан с ID {created_user.id}")

        # Ищем по email через CRUD
        found_by_email = get_user_by_email(db_session, email="crud@example.com")
        assert found_by_email is not None
        assert found_by_email.id == created_user.id
        print("✅ CRUD: Поиск по email работает")

        # Ищем по ID через CRUD
        found_by_id = get_user_by_id(db_session, user_id=created_user.id)
        assert found_by_id is not None
        assert found_by_id.email == created_user.email
        print("✅ CRUD: Поиск по ID работает")

    def test_crud_duplicate_prevention(self, db_session):
        """✅ Проверяет предотвращение дубликатов в CRUD"""
        print("🧪 Тест: CRUD - предотвращение дубликатов")

        from app.crud import create_user
        from app.schemas import UserCreate

        user_data = UserCreate(
            name="Duplicate Test",
            email="duplicate@example.com",
            bio="Test duplicate prevention"
        )

        # Первое создание - должно быть успешно
        user1 = create_user(db_session, user_data)
        assert user1 is not None

        # Второе создание с тем же email - должно вернуть None
        user2 = create_user(db_session, user_data)
        assert user2 is None

        print("✅ CRUD: Предотвращение дубликатов работает")


# 🔄 ТЕСТ ПОЛНОГО ЦИКЛА РАБОТЫ
def test_complete_user_workflow(client, db_session):
    """🔄 Проверяет полный цикл работы с пользователями"""
    print("🧪 Тест: Полный workflow пользователя")

    # 1. Создаем пользователя
    user_data = {
        "name": "Workflow User",
        "email": "workflow@example.com",
        "bio": "Testing complete workflow"
    }
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]
    print("✅ Шаг 1: Пользователь создан")

    # 2. Получаем пользователя по ID
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == user_data["email"]
    print("✅ Шаг 2: Пользователь найден по ID")

    # 3. Проверяем, что пользователь в общем списке
    list_response = client.get("/users/")
    assert list_response.status_code == 200
    users = list_response.json()
    user_emails = [user["email"] for user in users]
    assert user_data["email"] in user_emails
    print("✅ Шаг 3: Пользователь присутствует в общем списке")

    # 4. Пытаемся создать дубликат (должна быть ошибка)
    duplicate_response = client.post("/users/", json=user_data)
    assert duplicate_response.status_code == 400
    print("✅ Шаг 4: Дубликат корректно отклонен")

    print("🎉 Полный workflow тест пройден успешно!")


