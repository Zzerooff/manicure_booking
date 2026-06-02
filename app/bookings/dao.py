
from app.bookings.models import Booking
from app.dao.base import BaseDAO
from sqlalchemy import text
from app.database import async_session_maker

class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add_booking(cls, booking: Booking) -> Booking:
        async with async_session_maker() as session:
            session.add(booking)
            await session.commit()
            await session.refresh(booking)

            return booking


class SlotRepository:
    async def is_occupied(self, date_slot: str) -> bool:
        """Try use raw-SQL instead ORM to check slot availability"""

        async with async_session_maker() as session:
            result = session.execute(
                text(
                    "SELECT booking_time \
                    FROM public.bookings \
                    WHERE booking_date = :booking_date"
                ),
                {"booking_date": date_slot},
            )
            return result.first() is not None

    async def is_available(self, date_slot: str) -> bool:
        occupied = await self.is_occupied(date_slot)
        return not occupied
