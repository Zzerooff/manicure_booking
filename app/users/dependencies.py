from datetime import UTC, datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app import settings
from app.exceptions import (
    BadTokenFormatException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.dao import UserDAO
from app.users.models import AnonymousUser, User

ACCESS_TOKEN = "login_access_token"
SUB = "sub"
EXP = "exp"


def get_token(request: Request):
    token: str | None = request.cookies.get(ACCESS_TOKEN)
    return token


async def get_current_user(
    token: str = Depends(get_token),
) -> AnonymousUser | User:
    if not token:
        return AnonymousUser()

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise BadTokenFormatException
    expires = payload.get(EXP)

    if (not expires) or (int(expires) < datetime.now(UTC).timestamp()):
        raise TokenExpiredException
    user_id = payload.get(SUB)

    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException
    return user


async def get_current_user_optional(request: Request) -> AnonymousUser | User:
    try:
        token = get_token(request)
        return await get_current_user(token=token)
    except Exception:
        return AnonymousUser()
