import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("check@check.com", "check", 200),
        ("check@check.com", "check", 401),
        ("chec@chec.com", "chec", 200),
        ("check", "check", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("anna@example.com", "anna", 200),
        ("anna@example.com", "wrong", 401),
        ("wrong@info.com", "wrong", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
