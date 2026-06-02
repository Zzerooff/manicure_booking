import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "user_id, email, exist_present",
    [
        (2, "maria@example.com", True),
        (3, "elena@example.com", True),
        (999, "...", False),
    ],
)
async def test_user_find_by_id(user_id, email, exist_present):
    user = await UserDAO.find_by_id(user_id)
    if exist_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
