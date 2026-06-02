from pathlib import Path

from PIL import Image

from app.tasks.celery import celery_app

PREFIX_PATH = "resized"


@celery_app.task(name="resize_picture")
def resize_picture(
    path: str,
    width: int,
    height: int,
):
    image_path = Path(path)
    image = Image.open(image_path)
    save_path = image_path.parent / f"{PREFIX_PATH}_{width}x{height}_{image_path.name}"
    image.resize((width, height)).save(save_path)
