from datetime import datetime, date, time
from typing import Any, List, Optional

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    user_id: int
    calendar_id: int
    wish_list: List[Any]
    booking_date: date
    booking_time: time
    total_price: float
    duration: int
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
