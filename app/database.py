from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.get_test_database_url
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.get_database_url
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный контекстный менеджер (зависимость) для получения сессии БД.
    Гарантированно закрывает сессию после завершения запроса.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
