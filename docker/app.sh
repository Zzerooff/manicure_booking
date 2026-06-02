#!/bin/bash

# Функция для ожидания доступности порта базы данных через Python
wait_for_db() {
  echo "Waiting for postgres..."
  python -c "
import socket
import time

while True:
    try:
        # Проверяем порт контейнера manicure_postgres
        with socket.create_connection(('manicure_postgres', 5432), timeout=1):
            break
    except OSError:
        time.sleep(0.2)
"
  echo "PostgreSQL started!"
}

# 1. Железно дожидаемся базу данных
wait_for_db

# 2. Запускаем наполнение базы
echo "Запуск скрипта наполнения базы данных..."
python /manicure_natali/fill_db.py

# 3. Запускаем сервер в зависимости от режима
if [ "$MODE" == "DEV" ]; then
    echo "Running in DEVELOPMENT mode"
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in PRODUCTION mode"
    gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
fi