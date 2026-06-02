import pytest
from httpx import ASGITransport, AsyncClient

from app.bookings.models import Booking
from app.calendar.models import Calendar
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.exceptions import InvalidDataException
from app.main import app
from app.wishes.models import Wish
from app.users.models import User
from app.utils import open_mock_json

MODELS_MAP = [User, Wish, Calendar, Booking]


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():

    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        print("--- DROP AND CREATE TABLES ---")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        for model_class in MODELS_MAP:
            schema_class = model_class.metadata_schema
            data = open_mock_json(model_class.__tablename__, schema_class)

            if data:
                await session.execute(model_class.__table__.insert(), data)
            else:
                raise InvalidDataException

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def authenticated_ac():

    assert settings.MODE == "TEST"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login_response = await ac.post(
            "/auth/login", json={"email": "anna@example.com", "password": "anna"}
        )

        assert login_response.status_code == 200

        if login_response.cookies:
            ac.cookies.update(login_response.cookies)

        yield ac
