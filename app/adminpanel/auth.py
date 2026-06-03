from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.users.auth import authenticate_user, create_access_token, verify_password
from app.users.dao import UserDAO  # проверь правильность пути к вашему DAO
from app.users.dependencies import get_current_user

SUB = "sub"
TOKEN = "token"


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = str(form.get("username")).strip()
        password = str(form.get("password")).strip()

        user = await UserDAO.find_one_or_none(email=email)

        if not user:
            return False

        is_match = verify_password(password, user.password_hash)

        if is_match and getattr(user, "is_admin", False):
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True

        user = await authenticate_user(email=email, password=password)
        if user:
            access_token = create_access_token({SUB: str(user.id)})
            request.session.update({TOKEN: access_token})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get(TOKEN)

        if not token:
            return False

        user = await get_current_user(token)
        if not user:
            return False

        return True


authentication_backend = AdminAuth(secret_key="...")
