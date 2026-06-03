from datetime import date, time
from typing import Any

from fastapi import APIRouter, Depends, Query, status

from app.bookings.booking_service import BookingService
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование слота"],
)


@router.get("", description="Возвращает все брони текущего пользователя")
async def get_my_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
    return list(await BookingDAO.find_all(user_id=user.id))


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Бронирует слот записи текущего пользователя",
)
async def create_booking(
    date: date = Query(..., description="Дата слота формата YYYY-MM-DD"),
    time_slot: time = Query(..., description="Время слота например 10:00"),
    wish_list: list[int] = Query(..., description="Перечисление услуг 1,2,3"),
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    booking = await BookingService.create_new_booking(
        date=date,
        time_slot=time_slot,
        wish_list=wish_list,
        user=user,
    )
    return {"booking_id": booking.id, "message": "Booking created"}
