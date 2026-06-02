from sqladmin import ModelView

from app.bookings.models import Booking
from app.calendar.models import Calendar
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [c.name for c in User.__table__.c]
    column_details_exclude_list = [User.password_hash]

    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Booking):
    column_list = [Booking.user] + [c.name for c in Booking.__table__.c]
    name = "Брони"
    name_plural = "Бронирование"
    icon = "fa-solid fa-user"


class CalendarAdmin(ModelView, model=Calendar):
    column_list = [c.name for c in Calendar.__table__.c]
    can_delete = False
    name = "Слоты"
    name_plural = "Календарь"
    icon = "fa-solid fa-user"
