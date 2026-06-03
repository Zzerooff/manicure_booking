from datetime import date, datetime, time

from pydantic import BaseModel, Field


class SCalendar(BaseModel):
    id: int
    date: date
    is_available: bool = Field(default=True)
    working_hours_start: time
    working_hours_end: time
    break_start: time | None = None
    break_end: time | None = None
    slot_duration: int = Field(default=150, description="Длительность слота в минутах")
    available_slots: list[time]
    max_bookings_per_day: int = Field(default=4)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
