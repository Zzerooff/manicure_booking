# app/users/models.py
from pydantic import ConfigDict
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.users.schemas import SUser


class User(Base):
    __tablename__ = "users"
    model_config = ConfigDict(ser_json_bytes="utf-8")  # Для корректной сериализации

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bookings = relationship(
        "Booking", back_populates="user", cascade="all, delete-orphan"
    )

    metadata_schema = SUser

    @property
    def is_authenticated(self) -> bool:
        """
        Если этот объект пользователя был успешно получен из БД,
        значит пользователь прошел аутентификацию.
        """
        return True

    def __str__(self):
        return f"User {self.email}"


class AnonymousUser:
    """Класс-заглушка для неавторизованного пользователя"""

    @property
    def is_authenticated(self) -> bool:
        return False
