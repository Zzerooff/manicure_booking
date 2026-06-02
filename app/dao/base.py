from typing import TypeVar, Type, Generic, Any, Sequence

from sqlalchemy import insert, select, delete

from app.database import async_session_maker
from app.database import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: Type[T]

    @classmethod
    async def find_by_id(cls, model_id) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            calendar = await session.execute(query)
            return calendar.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            calendar = await session.execute(query)
            return calendar.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by: Any) -> Sequence[T]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            calendar = await session.execute(query)
            return calendar.scalars().all()

    @classmethod
    async def add(cls, **data: Any) -> Any:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_by_id(cls, model_id) -> Any:
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_by_date(cls, **date: Any) -> Any:
        async with async_session_maker() as session:
            query = delete(cls.model)

            date_start = date.pop("date_start", None)
            date_end = date.pop("date_end", None)

            if date_start or date_end:
                if date_start:
                    query = query.where(cls.model.date >= date_start)
                if date_end:
                    query = query.where(cls.model.date <= date_end)

            if date:
                query = query.where(**date)

            await session.execute(query)
            await session.commit()
