import os
import uuid
from http import HTTPStatus
from pathlib import Path

from fastapi import HTTPException
from httpx import AsyncClient

from functools import lru_cache

from src.configs.config import settings, Settings
from src.schemas.api.v1.image import ResponsePutImage


class ImageService:
    _http_client: AsyncClient

    def __init__(self, static_settings: Settings, http_client: AsyncClient):
        self.__static = static_settings.static
        self.__http_client = http_client
        self.__file_dir_path = os.path.join(
            self.__static.main_dir, self.__static.mem_images_dir
        )
        p = Path(self.__file_dir_path)
        p.mkdir(parents=True, exist_ok=True)

    async def remove_from_disc(self, file_name: str) -> None:
        file_extension = None
        if file.content_type is not None:
            _, file_extension = file.content_type.split("/")

        file.filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = str(os.path.join(self.__file_dir_path, file.filename))

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return f"{self.__file_dir_url}{file.filename}"

    async def put(self, file_name: str) -> ResponsePutImage:
        image_url = ""
        image_key = ""

        async with self.__http_client as client:
            response = await client.post(
                url=self.__s3_saver.url, data={"file_url": file_url}
            )
        data = response.json()
        if data:
            image_url, image_key = data.get("image"), data.get("image_key")

        return image_url, image_key

    async def remove(self, file_key: str) -> str:
        url = self.__s3_saver.url + f"/{file_key}"

        async with self.__http_client as client:
            response = await client.delete(url=url)

        if response.status_code == 200:
            return file_key
        else:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"error deleting a file from s3 storage. status_code={response.status_code}",
            )


@lru_cache
def get_image_service() -> ImageService:
    return ImageService(settings, AsyncClient())
