# app/calendar/models.py
from pydantic import ConfigDict
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.calendar.schemas import SCalendar
from app.database import Base


class Calendar(Base):
    __tablename__ = "calendar"
    model_config = ConfigDict(ser_json_bytes="utf-8")  # Для корректной сериализации

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)  # Дата
    is_available = Column(Boolean, default=True)  # Доступен ли день
    working_hours_start = Column(
        String, nullable=False, default="10:00"
    )  # Начало работы
    working_hours_end = Column(String, nullable=False, default="20:00")  # Конец работы
    break_start = Column(String, nullable=True, default="14:00")  # Начало перерыва
    break_end = Column(String, nullable=True, default="15:00")  # Конец перерыва
    slot_duration = Column(
        Integer, default=150
    )  # Длительность слота в минутах (2.5 часа = 150 минут)
    available_slots = Column(JSONB, default=list)  # Доступные временные слоты
    max_bookings_per_day = Column(
        Integer, default=4
    )  # Максимум записей в день (при 2.5ч интервале при 10-20ч = 4 слота)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bookings = relationship("Booking", back_populates="calendar")

    metadata_schema = SCalendar

    def __str__(self):
        return f"Slot {self.id} {self.date}"
