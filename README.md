# Manicure Booking API 💅

Бэкенд-приложение для автоматизации записи в салон красоты. Реализует логику бронирования времени, управления услугами и администрирования процессов.

## 🛠 Технологический стек
* **Фреймворк:** FastAPI
* **База данных:** PostgreSQL
* **ORM & Миграции:** SQLAlchemy, Alembic
* **Контейнеризация:** Docker, Docker Compose
* **Тестирование:** Pytest
* **Валидация данных:** Pydantic v2
* **Линтеры/Форматтеры:** Ruff

## 🚀 Быстрый старт

1. Клонируйте репозиторий
```bash
    git clone https://github.com/Zzerooff/manicure_booking.git
    cd manicure_booking
```
2. Подготовьте окружение
```bash
    ./setup_project.sh
```
3. Запустите проект
```bash
    docker-compose up --build
```
4. Проверьте работу. Перейдите в документацию Swagger
```bash
   http://localhost:8000/docs
```
Далее выполните /register -> /login -> /pages/calendar

## 💻 Локальный запуск

1. Создайте и активируйте виртуальное окружение:
```bash
    python -m venv .venv
    source .venv/bin/activate
```
или для Windows:

```bash
    python -m venv .venv
    .venv\Scripts\activate
```

2. Установите зависимости: 
```bash
    pip install -r requirements.txt
```

3. Примените миграции Alembic: 
```bash
    alembic upgrade head
```

4. Запустите сервер: 
```bash
    uvicorn app.main:app --reload
```

## 🧪 Тестирование 
```bash
    pytest -s -vv
```

* **Async-first:** Приложение полностью написано с использованием асинхронного подхода (FastAPI + `asyncpg` + асинкт-сессии SQLAlchemy).
* **Слоистая архитектура:** Использование паттерна DAO (Data Access Object) для изоляции логики работы с базой данных от бизнес-логики эндпоинтов.
* **Безопасность:** Реализована ролевая модель (клиент / администратор) и JWT-аутентификация.
