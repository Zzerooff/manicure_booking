from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.exceptions import IncorrectEmailOrPasswordException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import SUserAuth, SUserCurrent

SUB = "sub"

LOGIN_ACCESS_TOKEN = "login_access_token"

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register(user_date: SUserAuth):
    try:
        existing_user = await UserDAO().find_one_or_none(email=user_date.email)
        if existing_user:
            raise IncorrectEmailOrPasswordException
        hashed_password = get_password_hash(user_date.password)

        await UserDAO.add(
            email=user_date.email,
            password_hash=hashed_password,
            is_active=True,
            is_admin=False,
        )
    except (HTTPException, Exception) as e:
        raise e


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    try:
        user = await authenticate_user(user_data.email, user_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        access_token = create_access_token({SUB: str(user.id)})
        response.set_cookie(LOGIN_ACCESS_TOKEN, access_token, httponly=True)
        return {"access_token": access_token}
    except (HTTPException, Exception) as e:
        raise e


@router.get("/logout")
async def logout_user(response: Response):
    try:
        response.delete_cookie(LOGIN_ACCESS_TOKEN)
        return "User logged out"
    except (HTTPException, Exception) as e:
        raise e


@router.get("/me", response_model=SUserCurrent)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    Благодаря response_model, наружу отдаются только безопасные поля.
    """
    return current_user
