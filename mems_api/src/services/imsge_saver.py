import os
import uuid
from pathlib import Path

from fastapi import UploadFile
from httpx import AsyncClient

from functools import lru_cache

from src.configs.config import settings


class ImageSaver:
    _http_client: AsyncClient

    def __init__(self):
        self._http_client = AsyncClient()

    async def save(self, file: UploadFile) -> str:
        static_path = str(
            os.path.join(settings.static.main_dir, settings.static.mem_images_dir)
        )
        p = Path(static_path)
        p.mkdir(parents=True, exist_ok=True)

        file_extension = None
        if file.content_type is not None:
            _, file_extension = file.content_type.split("/")

        file.filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = str(os.path.join(static_path, file.filename))

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return f"{settings.static.main_dir}/{settings.static.mem_images_dir}/{file.filename}"

    async def save_to_s3(self, file_path: str) -> str:
        pass


@lru_cache
def get_image_sever_service() -> ImageSaver:
    return ImageSaver()
