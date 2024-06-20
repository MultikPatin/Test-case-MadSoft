import os
from contextlib import asynccontextmanager
from pathlib import Path


from functools import lru_cache

from src.configs.config import settings, Settings
from src.schemas.api.v1.image import ResponsePutImage

from aiobotocore.session import get_session, AioSession


class ImageService:
    __session: AioSession

    def __init__(self, settings: Settings, session: AioSession):
        self.__static = settings.static
        self.__file_dir_path = os.path.join(
            self.__static.main_dir, self.__static.mem_images_dir
        )
        p = Path(self.__file_dir_path)
        p.mkdir(parents=True, exist_ok=True)

        self.config = {
            "aws_access_key_id": settings.s3.access_key,
            "aws_secret_access_key": settings.s3.secret_key,
            "endpoint_url": settings.s3.endpoint_url,
        }
        self.bucket_name = settings.s3.bucket_name
        self.__session = session

    @asynccontextmanager
    async def get_client(self):
        async with self.__session.create_client("s3", **self.config) as client:
            yield client

    @staticmethod
    async def _remove_from_disc(file_path: str) -> None:
        p = Path(file_path)
        p.unlink()

    async def put(self, file_name: str) -> ResponsePutImage:
        file_path = os.path.join(self.__file_dir_path, file_name)
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=file_name,
                        Body=file,
                    )
        except Exception:
            pass

        endpoint_url = self.config["endpoint_url"]
        image_url = f"{endpoint_url}/{self.bucket_name}/{file_name}"

        await self._remove_from_disc(file_path)

        return ResponsePutImage(
            image_url=image_url,
            image_key=file_name,
        )

    async def remove(self, file_key: str) -> str:
        try:
            async with self.get_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=file_key,
                )
        except Exception:
            pass

        return file_key


@lru_cache
def get_image_service() -> ImageService:
    return ImageService(settings, get_session())
