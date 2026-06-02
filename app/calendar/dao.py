
from app.calendar.models import Calendar
from app.dao.base import BaseDAO
from app.database import async_session_maker


class CalendarDAO(BaseDAO):
    model = Calendar

    @classmethod
    async def refresh_available_slots(cls, date, time_slot: str):
        async with async_session_maker() as session:
            calendar = await cls.find_one_or_none(session=session, date=date)

            if calendar and calendar.available_slots:
                calendar.available_slots = [
                    slot for slot in calendar.available_slots if slot != time_slot
                ]

                await session.commit()

    @classmethod
    async def take_up_current_slot(cls, session, calendar_id: int, slot_to_remove: str):
        calendar = await session.get(cls.model, calendar_id)

        if calendar and calendar.available_slots:
            calendar.available_slots = [
                slot for slot in calendar.available_slots if slot != slot_to_remove
            ]
