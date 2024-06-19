import os
import uuid
from pathlib import Path

from fastapi import UploadFile
from httpx import AsyncClient

from functools import lru_cache

from src.configs.config import settings, Settings


class ImageSaver:
    _http_client: AsyncClient

    def __init__(self, static_settings: Settings, http_client: AsyncClient):
        self.__static = static_settings.static
        self.__s3_saver = static_settings.s3_sever
        self.__http_client = http_client
        self.__file_dir_url = (
            f"{self.__static.main_dir}/{self.__static.mem_images_dir}/"
        )
        self.__file_dir_path = os.path.join(
            self.__static.main_dir, self.__static.mem_images_dir
        )
        p = Path(self.__file_dir_path)
        p.mkdir(parents=True, exist_ok=True)

    async def save_to_disc(self, file: UploadFile) -> str:
        file_extension = None
        if file.content_type is not None:
            _, file_extension = file.content_type.split("/")

        file.filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = str(os.path.join(self.__file_dir_path, file.filename))

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return f"{self.__file_dir_url}{file.filename}"

    async def put_to_s3(self, file_url: str) -> tuple[str, str]:
        file_name = file_url.split("/")[-1]
        image_url = ""
        image_key = ""

        async with self.__http_client as client:
            response = await client.put(
                url=self.__s3_saver.url_image, data={"file_name": file_name}
            )
        data = response.json()
        if data:
            image_url, image_key = data.get("image"), data.get("image_key")

        return image_url, image_key

    async def del_from_s3(self, file_key: str) -> int:
        url = self.__s3_saver.url_image + f"/{file_key}"

        async with self.__http_client as client:
            response = await client.delete(url=url)

        return response.status_code


@lru_cache
def get_image_saver_service() -> ImageSaver:
    return ImageSaver(settings, AsyncClient())
