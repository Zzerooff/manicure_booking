from datetime import UTC, datetime, timedelta

import passlib.context
from jose import jwt
from pydantic import EmailStr

from app import settings
from app.exceptions import UserIsNotPresentException, IncorrectEmailOrPasswordException
from app.users.dao import UserDAO

EXP = "exp"

pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password.strip())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({EXP: expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)

    if not user:
        raise UserIsNotPresentException

    if not verify_password(password, user.password_hash):
        raise IncorrectEmailOrPasswordException

    return user
