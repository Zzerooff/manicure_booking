from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class SWish(BaseModel):
    id: int
    name: str
    name_ru: str
    description: str
    duration: int
    price: float
    icon: str
    category: str
    is_active: bool
    order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @model_validator(mode="after")
    def set_name_ru_if_empty(self) -> "SWish":
        if self.name_ru:
            self.name = self.name_ru
        return self
