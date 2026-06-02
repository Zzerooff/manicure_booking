import asyncio
from datetime import datetime, timedelta

from sqlalchemy import text
from app.database import engine, Base  # Импортируем Base (убедись, что путь правильный)
from app.users.auth import get_password_hash

# Импортируем модели, чтобы Алхимия "увидела" их перед созданием таблиц


async def fill_db():
    # 1. Сначала ГАРАНТИРОВАННО создаем таблицы, если их нет в базе
    print("Проверка и создание таблиц...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы готовы.")

    # 2. Проверяем суммарное количество строк во ВСЕХ пользовательских таблицах
    async with engine.connect() as conn:
        check_all_tables_query = """
            SELECT COALESCE(SUM(n_live_tup), 0) 
            FROM pg_stat_user_tables;
        """
        result = await conn.execute(text(check_all_tables_query))
        total_rows = result.scalar()

        if total_rows > 0:
            print(
                f"База данных уже содержит данные ({total_rows} строк суммарно). Пропускаю автозаполнение."
            )
            return

    print("База абсолютно пуста. Начинаю генерацию дат и загрузку данных...")

    valid_hash = get_password_hash("123456")

    # Дальше идет твой неизмененный код (today = datetime.now().date(), queries = [...] и т.д.)
    today = datetime.now().date()

    # Генерируем даты динамически
    date_0 = today.strftime("%Y-%m-%d")  # Сегодня
    date_1 = (today + timedelta(days=1)).strftime("%Y-%m-%d")  # Завтра
    date_2 = (today + timedelta(days=2)).strftime("%Y-%m-%d")  # Послезавтра
    date_3 = (today + timedelta(days=3)).strftime("%Y-%m-%d")  # +3 дня
    date_4 = (today + timedelta(days=4)).strftime("%Y-%m-%d")  # +4 дня

    queries = [
        f"""
    -- 1. Вставка пользователей (конфликт проверяем по username)
    INSERT INTO users (name, username, email, phone, password_hash, is_active, is_admin, created_at, updated_at)
    VALUES 
        ('Анна Иванова', 'anna_i', 'anna@example.com', '+79001234567', '{valid_hash}', true, true, NOW(), NOW()),
        ('Мария Петрова', 'maria_p', 'maria@example.com', '+79007654321', '{valid_hash}', true, false, NOW(), NOW()),
        ('Елена Смирнова', 'elena_s', 'elena@example.com', '+79008887777', '{valid_hash}', true, false, NOW(), NOW()),
        ('Ольга Кузнецова', 'olga_k', 'olga@example.com', '+79009998888', '{valid_hash}', true, false, NOW(), NOW()),
        ('Татьяна Волкова', 'tatiana_v', 'tatiana@example.com', '+79005556666', '{valid_hash}', true, false, NOW(), NOW())
    ON CONFLICT (username) DO NOTHING;
    """,
        """
    -- 2. Вставка услуг (Конфликт переведен на гарантированный Primary Key ID)
    INSERT INTO wishes (id, name, name_ru, description, duration, price, icon, category, is_active, "order", created_at, updated_at)
    VALUES 
        (1, 'manicure', 'Маникюр', 'Классический маникюр с покрытием гель-лаком', 90, 1500, '💅', 'manicure', true, 1, NOW(), NOW()),
        (2, 'pedicure', 'Педикюр', 'Комплексный педикюр с уходом', 120, 2500, '🦶', 'pedicure', true, 2, NOW(), NOW()),
        (3, 'shellac', 'Шеллак', 'Покрытие гель-лаком', 60, 1200, '💅', 'coating', true, 3, NOW(), NOW()),
        (4, 'hand_care', 'Уход за руками', 'Парафинотерапия + массаж', 45, 800, '🧴', 'care', true, 4, NOW(), NOW()),
        (5, 'nail_art', 'Дизайн ногтей', 'Художественная роспись или стемпинг', 60, 1000, '🎨', 'design', true, 5, NOW(), NOW())
    ON CONFLICT (id) DO NOTHING;  
    """,
        f"""
    -- 3. Вставка календаря (Добавлена f-строка!)
    INSERT INTO calendar (date, is_available, working_hours_start, working_hours_end, break_start, break_end, slot_duration, available_slots, max_bookings_per_day, created_at, updated_at)
    VALUES 
        ('{date_0}', true, '10:00:00', '20:00:00', '13:00:00', '14:00:00', 150, '["10:00", "12:30", "15:00", "17:30"]', 4, NOW(), NOW()),
        ('{date_1}', true, '10:00:00', '20:00:00', '13:00:00', '14:00:00', 150, '["10:00", "12:30", "15:00", "17:30"]', 4, NOW(), NOW()),
        ('{date_2}', true, '10:00:00', '20:00:00', NULL, NULL, 150, '["10:00", "12:30", "15:00", "17:30"]', 4, NOW(), NOW()),
        ('{date_3}', false, '10:00:00', '20:00:00', NULL, NULL, 150, '[]', 0, NOW(), NOW()),
        ('{date_4}', true, '10:00:00', '18:00:00', NULL, NULL, 150, '["10:00", "12:30", "15:00"]', 3, NOW(), NOW())
    ON CONFLICT (date) DO NOTHING;
    """,
        f"""
    -- Вставка броней
    INSERT INTO bookings (user_id, calendar_id, wish_list, booking_date, booking_time, total_price, duration, status, notes, created_at, updated_at)
    VALUES 
        (1, 1, '[{{"id": 1, "name": "Маникюр", "price": 1500, "duration": 90}}]', '{date_0}', '10:00:00', 2700, 150, 'confirmed', 'Пожелания: яркий дизайн', NOW(), NOW()),
        (2, 1, '[{{"id": 1, "name": "Маникюр", "price": 1500, "duration": 90}}]', '{date_0}', '12:30:00', 1500, 90, 'confirmed', 'Наращивание не нужно', NOW(), NOW()),
        (3, 2, '[{{"id": 2, "name": "Педикюр", "price": 2500, "duration": 120}}]', '{date_1}', '15:00:00', 3300, 165, 'confirmed', 'Аллергия на латекс', NOW(), NOW()),
        (4, 3, '[{{"id": 1, "name": "Маникюр", "price": 1500, "duration": 90}}]', '{date_2}', '10:00:00', 2500, 150, 'confirmed', 'Хочу френч', NOW(), NOW()),
        (5, 5, '[{{"id": 3, "name": "Шеллак", "price": 1200, "duration": 60}}]', '{date_4}', '15:00:00', 1200, 60, 'confirmed', 'Снять старое покрытие', NOW(), NOW());
    """,
    ]

    async with engine.begin() as conn:
        for q in queries:
            await conn.execute(text(q))
        print("Данные успешно загружены!")


if __name__ == "__main__":
    asyncio.run(fill_db())
