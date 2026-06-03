#!/bin/bash

echo "--- Настройка проекта ---"

# 1. Создаем .env из примера
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Создан файл .env"
else
    echo "Файл .env уже существует, пропускаем."
fi

# 2. Исправляем окончания строк (CRLF -> LF) для всех .sh файлов
# Используем sed для удаления символов возврата каретки (\r)
echo "Исправление прав и форматов скриптов..."
find docker -name "*.sh" -exec sed -i 's/\r$//' {} \;

# 3. Даем права на исполнение
chmod +x docker/*.sh

echo "--- Готово! Можно запускать: docker-compose up --build ---"