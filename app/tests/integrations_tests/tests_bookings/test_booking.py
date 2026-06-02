from datetime import date

import pytest
from httpx import AsyncClient

from app.bookings.booking_service import BookingService
from app.bookings.dao import BookingDAO
from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "date, time_slot, wish_list, status_code, booked_slots",
    [
        ("2024-04-01", "10:00", [1, 2], 201, 2),
    ],
)
async def test_login_add_get_booking(
    date,
    time_slot,
    wish_list,
    status_code,
    booked_slots,
    authenticated_ac: AsyncClient,
):

    response = await authenticated_ac.post(
        "/bookings",
        params={
            "date": date,
            "time_slot": time_slot,
            "wish_list": wish_list,
        },
    )

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert response.status_code == 200
    assert len(response.json()) == booked_slots


async def test_add_and_get_booking(
    date_str="2024-04-02", time_slot_str="15:00", wish_list=[1, 2]
):
    booking_date = date.fromisoformat(date_str)

    user = await UserDAO.find_by_id(5)
    booking = await BookingService.create_new_booking(
        date=booking_date,
        time_slot=time_slot_str,
        wish_list=wish_list,
        user=user,
    )

    assert int(booking.user_id) == user.id  # type: ignore

    booking = await BookingDAO.find_by_id(booking.id)

    assert booking is not None
