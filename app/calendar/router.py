from fastapi import APIRouter

from app.calendar.dao import CalendarDAO
from app.calendar.fill_calendar import fill_for_days
from app.calendar.schemas import SCalendar

router = APIRouter(
    prefix="/calendar",
    tags=["Календарь"],
)


@router.get("")
# @cache(expire=30)
async def get_calendar() -> list[SCalendar]:
    result = await CalendarDAO.find_all()
    return list(result)


@router.post("")
async def fill_date_calendar(
    date_start: str,
    date_end: str,
) -> str:
    return await fill_for_days(date_start, date_end)


@router.delete("/days/{date}")
async def delete_by_day(
    date_start: str,
    date_end: str,
) -> None:
    return await CalendarDAO.delete_by_date(date_start, date_end)


@router.delete("/entries/{entry_id}")
async def delete_day_by_id(
    day_id: str,
) -> None:
    return await CalendarDAO.delete_by_id(day_id)
