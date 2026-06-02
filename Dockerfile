# Используем стабильную версию
FROM python:3.12-slim

# Исправляем mkdir
RUN mkdir /manicure_natali

WORKDIR /manicure_natali

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости (добавляем без кэша, чтобы образ был меньше)
RUN pip install -r requirements.txt

# Копируем остальной код
COPY . .

RUN chmod a+x /manicure_natali/docker/*.sh

# Для FastAPI / ASGI приложений
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]