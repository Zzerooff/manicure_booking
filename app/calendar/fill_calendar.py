from datetime import datetime, timedelta

from app.calendar.models import Calendar
from app.database import async_session_maker

TABLE_NAME = Calendar.__tablename__

WORKING_HOURS_START = "10:00"
WORKING_HOURS_END = "20:00"
BREAK_START = "13:00"
BREAK_END = "14:00"
SLOT_DURATION = 150
AVAILABLE_SLOTS = ["10:00", "12:30", "15:00", "17:30"]
MAX_BOOKINGS_PER_DAY = 4

START_DAY, ONE_DAY = 1, 1


async def fill_for_days(date_start: str, date_end: str) -> str:
    """
    Вставка данных календаря
    (date, is_available, working_hours_start, working_hours_end, break_start, break_end, slot_duration, available_slots, max_bookings_per_day, created_at, updated_at)
    ('2024-04-01', true, '10:00:00',        '20:00:00',         '13:00:00',  '14:00:00', 150,           '["10:00", "12:30", "15:00", "17:30"]', 4,  NOW(), NOW()),
    """
    ds = datetime.strptime(date_start, "%Y-%m-%d")
    de = datetime.strptime(date_end, "%Y-%m-%d")
    days = (de - ds).days + ONE_DAY  # cuz '2026-01-05' - '2026-01-01' = 4 days, need 5

    calendars = []

    for i in range(days):
        current_date = ds + timedelta(days=i)
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
        async with session.begin():
            session.add_all(calendars)

    return f"Filled calendar for {days} days"
