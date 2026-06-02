# app/wishes/dao.py
from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.wishes.models import Wish


class WishesDAO(BaseDAO):
    model = Wish

    @classmethod
    async def get_wishes_by_ids(cls, wish_ids: list[int]) -> list[Wish]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id.in_(wish_ids))
            result = await session.execute(query)
            return list(result.scalars().all())
