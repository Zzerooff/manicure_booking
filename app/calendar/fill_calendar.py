from datetime import datetime, timedelta, time

from app.calendar.models import Calendar
from app.database import async_session_maker

TABLE_NAME = Calendar.__tablename__

WORKING_HOURS_START = time(10, 0)
WORKING_HOURS_END = time(20, 0)
BREAK_START = time(13, 0)
BREAK_END = time(14, 0)
SLOT_DURATION = 150
AVAILABLE_SLOTS = [time(10, 0), time(12, 30), time(15, 0), time(17, 30)]
MAX_BOOKINGS_PER_DAY = 4

ONE_DAY = 1


async def fill_for_days(date_start: str, date_end: str) -> str:
    ds = datetime.strptime(date_start, "%Y-%m-%d")
    de = datetime.strptime(date_end, "%Y-%m-%d")

    days = (de - ds).days + ONE_DAY
    if days <= 0:
        return "Ошибка: Дата начала больше даты конца!"

    calendars = []

    for i in range(days):
        current_date = (ds + timedelta(days=i)).date()
        calendar = Calendar(
            date=current_date,
            is_available=True,
            working_hours_start=WORKING_HOURS_START,
            working_hours_end=WORKING_HOURS_END,
            break_start=BREAK_START,
            break_end=BREAK_END,
            slot_duration=SLOT_DURATION,
            available_slots=AVAILABLE_SLOTS,
            max_bookings_per_day=MAX_BOOKINGS_PER_DAY,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        calendars.append(calendar)

    async with async_session_maker() as session:
        session.add_all(calendars)
        try:
            await session.commit()
            return f"Успешно добавлено {days} дней в календарь"
        except Exception as e:
            await session.rollback()
            return f"Ошибка при вставке: {e}"
