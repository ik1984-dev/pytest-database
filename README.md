# pytest-database

Проект для тестирования базы данных на основе современного стека технологий: **PostgreSQL, React, Pytest, FastAPI**.

## 🚀 Технологии

- **Backend**: FastAPI, PostgreSQL, Pytest
- **Frontend**: React, Node.js
- **База данных**: PostgreSQL
- **Тестирование**: Pytest с плагинами для работы с БД

## 📋 Предварительные требования

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Git

## 🛠️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/ik1984-dev/pytest-database
cd pytest-database

```

## Установка
### Бекенд:
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Фронтенд:
```bash
cd frontend
npm install
cd ..
```

# Запуск проекта
## Бекенд:
```bash
cd backend
python backend/run.py
```

### Фронтенд:
```bash
cd frontend
npm start
```


## Запуск тестов
```bash
cd backend
python backend/run.py

or

python.exe -m pytest .\tests\ -v -s
```

## Использованные библиотеки

Python (бекенд):

•	FastAPI - современный веб-фреймворк для создания API

•	SQLAlchemy - ORM для работы с базой данных

•	Pydantic - валидация данных и сериализация

•	python-dotenv - загрузка переменных окружения

•	Uvicorn (неявно) - ASGI сервер для запуска FastAPI

•	psycopg2 - это драйвер PostgreSQL для Python, который позволяет приложениям подключаться к базе данных PostgreSQL и выполнять SQL-запросы.


JavaScript/React (фронтенд):

•	React - библиотека для построения пользовательских интерфейсов

•	ReactDOM - рендеринг React в браузерный DOM

•	Axios - HTTP клиент для API запросов

•	Web Vitals - мониторинг производительности веб-приложения



Тестирование:

•	Jest (через React Scripts) - фреймворк для тестирования

•	React Testing Library - утилиты для тестирования React компонентов

2. Используемые протоколы API:

REST API (основной)

•	HTTP/1.1 - протокол передачи данных

•	RESTful архитектура:

o	POST /users/ - создание пользователя

o	GET /users/ - получение списка пользователей

o	GET /users/{id} - получение конкретного пользователя


Дополнительные протоколы:

•	CORS - межсайтовые запросы между localhost:3000 и бекендом

•	JSON - формат данных для API коммуникации

•	PostgreSQL Protocol - общение с базой данных

Сетевые протоколы:

•	TCP/IP - базовый транспортный протокол

•	HTTP - протокол прикладного уровня для API

ORM - Object-Relational Mapping (Объектно-реляционное отображение) - технология, которая позволяет работать с базой данных используя объекты programming языка вместо SQL запросов.

ASGI - Asynchronous Server Gateway Interface (Асинхронный серверный шлюз интерфейс) - современный стандарт Python для асинхронных веб-приложений, который пришел на смену WSGI.

DOM - Document Object Model (Объектная модель документа) - древовидное представление HTML документа, которое позволяет JavaScript взаимодействовать и изменять веб-страницу.


Взаимодействие протоколов и библиотек:

Frontend (React) → Backend (FastAPI)

React Component → Axios → HTTP/1.1 → FastAPI (Uvicorn)


Backend (FastAPI) → Database (PostgreSQL)

FastAPI → SQLAlchemy → psycopg2 → PostgreSQL Protocol → PostgreSQL Server

Детальная цепочка:

1.	Фронтенд запрос:
UserForm → Axios (HTTP клиент) → HTTP запрос → FastAPI эндпоинт

2.	Бекенд обработка:
FastAPI → Pydantic (валидация) → SQLAlchemy (ORM) → psycopg2 (драйвер)

3.	База данных:
psycopg2 → PostgreSQL Protocol (бинарный) → TCP/IP → PostgreSQL сервер

4.	Обратный путь:
PostgreSQL → TCP/IP → psycopg2 → SQLAlchemy → Pydantic → JSON → HTTP ответ → React

Дополнительные протоколы:
•	CORS - управляет доступом между портами 3000 и бекендом
•	WebSocket (ASGI) - для асинхронной работы FastAPI

npm (Node Package Manager) - менеджер пакетов для JavaScript, который используется для установки и управления зависимостями в вашем React-проекте.

