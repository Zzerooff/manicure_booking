from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.calendar.models import Calendar
from app.calendar.schemas import SCalendar
from app.dao.base import BaseDAO
from app.database import async_session_maker
from datetime import date, time


class CalendarDAO(BaseDAO):
    model = Calendar

    @classmethod
    async def get_by_date(cls, session, date: date):
        query = select(Calendar).where(Calendar.date == date)
        result = await session.execute(query)
        calendar_model = result.scalar_one_or_none()

        if calendar_model is None:
            return None

        return SCalendar.model_validate(calendar_model)

    @classmethod
    async def refresh_available_slots(cls, date, time_slot: time):
        async with async_session_maker() as session:
            calendar = await cls.find_one_or_none(session=session, date=date)

            if calendar and calendar.available_slots:
                calendar.available_slots = [
                    slot for slot in calendar.available_slots if slot != time_slot
                ]

                await session.commit()

    @classmethod
    async def take_up_current_slot(
        cls, session, calendar_id: int, slot_to_remove: time
    ):
        calendar = await session.get(cls.model, calendar_id)

        if calendar and calendar.available_slots:
            calendar.available_slots = [
                slot for slot in calendar.available_slots if slot != slot_to_remove
            ]

        flag_modified(calendar, "available_slots")
