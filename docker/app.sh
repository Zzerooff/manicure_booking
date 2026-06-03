#!/bin/bash

wait_for_db() {
  local db_host="${DB_HOST:-db}"
  local db_port="${DB_PORT:-5432}"

  echo "Waiting for postgres at $db_host:$db_port..."
  python -c "
import socket
import time
import os

host = os.getenv('DB_HOST', 'db')
port = int(os.getenv('DB_PORT', 5432))

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            break
    except OSError:
        time.sleep(0.5)
"
  echo "PostgreSQL started!"
}

wait_for_db

echo "Применение миграций Alembic..."
alembic upgrade head

echo "Запуск скрипта наполнения базы данных..."
python fill_db.py
if [ "$MODE" == "DEV" ]; then
    echo "Running in DEVELOPMENT mode"
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in PRODUCTION mode"
    gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
fi