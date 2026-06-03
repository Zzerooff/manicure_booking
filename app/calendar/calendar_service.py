from datetime import datetime, timedelta
from typing import Any, Dict, Sequence

from app.calendar.models import Calendar
from app.wishes.models import Wish

from typing import Optional


async def generate_calendar_context(
    db_calendar_days: Sequence[Calendar],
    wish_list: Sequence[Wish],
    current_user: Optional[Any] = None,
) -> Dict[str, Any]:
    start_day_offset = db_calendar_days[0].date.weekday() if db_calendar_days else 0

    cleaned_days = [
        {
            "date": day.date,
            "is_available": bool(day.is_available),
            "available_slots": [
                t.strftime("%H:%M") for t in (day.available_slots or [])
            ],
        }
        for day in db_calendar_days
    ]

    return {
        "current_user": {
            "is_authenticated": getattr(current_user, "is_authenticated", False)
        },
        "start_day_offset": start_day_offset,
        "calendar_days": cleaned_days,
        "wish_list": [
            {"id": w.id, "name": w.name_ru, "icon": getattr(w, "icon", "💼")}
            for w in wish_list
        ],
    }


def generate_daily_slots(
    start_str: str,
    end_str: str,
    break_start_str: str | None,
    break_end_str: str | None,
    duration_minutes: int,
) -> list[dict]:
    """
    Генерирует массив слотов вида: [{"id": 1, "time": "10:00", "is_free": True}]
    """
    slots = []

    # Парсим строки времени в объекты datetime для удобства математики
    # Используем фиктивную дату, так как нам нужно только время
    dummy_date = datetime(2000, 1, 1)

    start_dt = datetime.combine(
        dummy_date, datetime.strptime(start_str, "%H:%M").time()
    )
    end_dt = datetime.combine(dummy_date, datetime.strptime(end_str, "%H:%M").time())

    b_start_dt = (
        datetime.combine(dummy_date, datetime.strptime(break_start_str, "%H:%M").time())
        if break_start_str
        else None
    )
    b_end_dt = (
        datetime.combine(dummy_date, datetime.strptime(break_end_str, "%H:%M").time())
        if break_end_str
        else None
    )

    current_dt = start_dt
    slot_id = 1

    while current_dt + timedelta(minutes=duration_minutes) <= end_dt:
        slot_start_time = current_dt.time()
        slot_end_time = (current_dt + timedelta(minutes=duration_minutes)).time()

        # Проверяем, пересекается ли слот с перерывом
        is_during_break = False
        if b_start_dt and b_end_dt:
            # Слот попадает в перерыв, если он начинается или идет во время перерыва
            if not (
                slot_end_time <= b_start_dt.time() or slot_start_time >= b_end_dt.time()
            ):
                is_during_break = True

        # Если слот не в перерыве, добавляем его
        if not is_during_break:
            slots.append(
                {
                    "id": slot_id,
                    "time": slot_start_time.strftime("%H:%M"),
                    "is_free": True,  # По умолчанию слот свободен
                }
            )
            slot_id += 1

        # Переходим к следующему слоту
        current_dt += timedelta(minutes=duration_minutes)

    return slots
