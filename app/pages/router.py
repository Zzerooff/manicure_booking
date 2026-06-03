from datetime import date, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.calendar.router import get_calendar
from app.database import get_db
from app.users.dependencies import get_current_user_optional

from sqlalchemy import select

from app.calendar.models import Calendar
from app.calendar.calendar_service import generate_calendar_context
from app.wishes.models import Wish

router = APIRouter(prefix="/pages", tags=["Фронтенд"])

templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def get_pages(request: Request, calendar=Depends(get_calendar)):
    return templates.TemplateResponse(
        name="slots.html", context={"request": request, "calendar": calendar}
    )


COUNT_DAYS = 30


@router.get(
    "/calendar",
    description="### [👉 Открыть страницу календаря в браузере](/pages/calendar)",
)
async def get_calendar_page(
    request: Request,
    current_user=Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    today = date.today()
    end_date = today + timedelta(days=COUNT_DAYS)

    calendar_query = (
        select(Calendar)
        .where(Calendar.date >= today, Calendar.date <= end_date)
        .order_by(Calendar.date.asc())
    )
    calendar_result = await db.execute(calendar_query)
    db_calendar_days = calendar_result.scalars().all()

    wish_query = select(Wish)
    wish_result = await db.execute(wish_query)
    db_wish_list = wish_result.scalars().all()

    context = await generate_calendar_context(
        db_calendar_days=db_calendar_days,
        wish_list=db_wish_list,
        current_user=current_user,
    )

    return templates.TemplateResponse(
        request=request, name="calendar.html", context=context
    )
