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
    .\setup_project.sh
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
