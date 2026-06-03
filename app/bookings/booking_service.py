from datetime import date, time

from sqlalchemy.exc import SQLAlchemyError

from app.bookings.dao import BookingDAO, SlotRepository
from app.bookings.models import Booking
from app.calendar.dao import CalendarDAO
from app.calendar.models import Calendar
from app.database import async_session_maker
from app.exceptions import SlotCantBeBooking, BookingCreationFailedException
from app.logger import logger
from app.users.models import User

CONFIRMED = "confirmed"


class BookingService:
    def __init__(self):
        self.slot_repository = SlotRepository()

    @classmethod
    async def create_new_booking(
        cls, date: date, time_slot: time, wish_list: list[int], user: User
    ):
        async with async_session_maker() as session:
            async with session.begin():
                calendar = await CalendarDAO.get_by_date(session, date)

                if not calendar or time_slot not in calendar.available_slots:
                    raise SlotCantBeBooking()

                cls._validate_calendar_time_slot(calendar, time_slot)

                try:
                    total_price, total_duration = cls._calculate_totals(wish_list)

                    new_booking_object = Booking(
                        user_id=user.id,
                        calendar_id=calendar.id,
                        booking_date=date,
                        booking_time=time_slot,
                        wish_list=wish_list,
                        total_price=total_price,
                        duration=total_duration,
                        status=CONFIRMED,
                    )
                    booking = await BookingDAO.add_booking(new_booking_object)

                    await CalendarDAO.take_up_current_slot(
                        session=session,
                        calendar_id=calendar.id,
                        slot_to_remove=time_slot,
                    )

                    return booking

                except SQLAlchemyError:
                    logger.error(
                        msg="Database error while adding booking",
                        extra={
                            "user_id": user.id,
                            "date": date,
                            "time_slot": time_slot,
                        },
                        exc_info=True,
                    )
                    raise BookingCreationFailedException()

                except Exception as e:
                    logger.critical(
                        msg="Unexpected error in create booking logic:",
                        extra={
                            "user_id": user.id,
                            "date": date,
                            "time_slot": time_slot,
                        },
                        exc_info=True,
                    )
                    raise e

    @staticmethod
    def _validate_calendar_time_slot(calendar: Calendar, time_slot: time) -> None:
        """Проверяет существование дня и наличие свободного слота в нем"""

        if not calendar or time_slot not in calendar.available_slots:
            raise SlotCantBeBooking()

    @staticmethod
    def _calculate_totals(wish_list: list) -> tuple[int, int]:
        if wish_list and isinstance(wish_list[0], dict):
            return (
                sum(i.get("price", 0) for i in wish_list),
                sum(i.get("duration", 0) for i in wish_list),
            )
        return 0, 0
