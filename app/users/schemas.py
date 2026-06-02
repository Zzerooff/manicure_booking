from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=50)


class SUserCurrent(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class SUser(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    password_hash: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
