from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field


class SCalendar(BaseModel):
    id: int
    date: date
    is_available: bool = Field(default=True)
    working_hours_start: str
    working_hours_end: str
    break_start: str | None = None
    break_end: str | None = None
    slot_duration: int = Field(default=150, description="Длительность слота в минутах")
    available_slots: List[str] = Field(
        default_factory=list, description="Доступные временные слоты"
    )
    max_bookings_per_day: int = Field(default=4)
    created_at: datetime
    updated_at: datetime
