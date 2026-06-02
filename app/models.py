# ruff: noqa # fmt: off # flake8: noqa
# app/models.py

from app.database import Base  # Импорт вашего базового класса
from app.users.models import User
from app.bookings.models import Booking
from app.calendar.models import Calendar
from app.wishes.models import Wish

# Теперь Base "знает" обо всех этих моделях, так как они были импортированы
