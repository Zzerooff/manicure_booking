# app/wishes/models.py
from pydantic import ConfigDict
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base
from app.wishes.schemas import SWish


class Wish(Base):
    __tablename__ = "wishes"
    model_config = ConfigDict(ser_json_bytes="utf-8")  # Для корректной сериализации

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # Название услуги
    name_ru = Column(String, nullable=True)  # Русское название
    description = Column(Text, nullable=True)  # Описание
    duration = Column(Integer, nullable=False)  # Длительность в минутах
    price = Column(Float, nullable=False)  # Цена
    icon = Column(String, nullable=True)  # Иконка (URL или имя файла)
    category = Column(
        String, nullable=True
    )  # Категория (маникюр, педикюр, покрытие и т.д.)
    is_active = Column(Boolean, default=True)
    order = Column(Integer, default=0)  # Порядок отображения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    metadata_schema = SWish

    def __repr__(self):
        return f"<Wish(id={self.id}, name={self.name}, name_ru={self.name_ru}, price={self.price})>"
