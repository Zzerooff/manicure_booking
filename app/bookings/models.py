# app/bookings/models.py
from pydantic import ConfigDict
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Date,
    Time,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.bookings.schemas import SBooking
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"
    model_config = ConfigDict(ser_json_bytes="utf-8")  # Для корректной сериализации

    id = Column(Integer, primary_key=True, index=True)

    # Внешние ключи
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    calendar_id = Column(
        Integer, ForeignKey("calendar.id", ondelete="CASCADE"), nullable=False
    )

    # Информация о брони
    wish_list = Column(
        JSON, nullable=True
    )  # Список услуг: [{"id": 1, "name": "Маникюр", "price": 1000}, ...]
    booking_date = Column(Date, nullable=True)  # Дата брони
    booking_time = Column(Time, nullable=True)  # Время брони
    total_price = Column(Float, nullable=True)  # Общая цена
    duration = Column(Integer, nullable=True)  # Общая длительность в минутах

    # Дополнительная информация
    status = Column(
        String, default="confirmed"
    )  # confirmed, cancelled, completed, no_show
    notes = Column(Text, nullable=True)  # Комментарии к заказу
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="bookings")
    calendar = relationship("Calendar", back_populates="bookings")

    metadata_schema = SBooking

    def __str__(self):
        return f"User id {self.user_id}"
