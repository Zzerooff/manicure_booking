import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import resize_picture

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/wish")
async def add_wish_image(
    name: int,
    file: UploadFile,
    width: int,
    height: int,
):
    image_path = f"app/static/images/{name}.webp"
    with open(image_path, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)

    resize_picture.delay(image_path, width, height)
