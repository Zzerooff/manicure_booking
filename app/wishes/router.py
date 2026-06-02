from fastapi import APIRouter

from app.wishes.dao import WishesDAO

router = APIRouter(
    prefix="/wishes",
    tags=["Список услуг"],
)


@router.get("")
async def get_wish_list():
    return await WishesDAO.find_all()


@router.get("")
async def get_wish_by_id(id: int):
    return await WishesDAO.find_by_id(id)
