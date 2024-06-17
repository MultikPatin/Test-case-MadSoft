from functools import lru_cache
from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException

from src.db.entities.mem import Mem
from src.schemas.api.v1.mem import (
    MemCreate,
    MemUpdate,
    ResponseMemPaginated,
)
from src.schemas.db.mem import MemDB
from src.services.base import BaseService
from src.db.repositories.mem import (
    MemRepository,
    get_mem_repository,
)
from src.services.imsge_saver import ImageSaver, get_image_saver_service


class MemService(
    BaseService[
        MemDB,
        ResponseMemPaginated,
        MemCreate,
        MemUpdate,
    ]
):
    def __init__(
        self,
        repository: MemRepository,
        image_sever_service: ImageSaver,
        model: type[MemDB],
    ):
        super().__init__(repository, model)
        self._image_sever_service = image_sever_service

    async def create(self, instance: MemCreate) -> MemDB:
        (
            instance.image_url,
            instance.image_key,
        ) = await self._image_sever_service.put_to_s3(instance.image_url)
        obj: Any = await self._repository.create(instance)
        model = self._model.model_validate(obj, from_attributes=True)  # type: ignore
        return model

    async def update(self, instance_uuid: UUID, instance: MemUpdate) -> MemDB:
        (
            instance.image_url,
            instance.image_key,
        ) = await self._image_sever_service.put_to_s3(instance.image_url)
        obj: Any = await self._repository.update(instance_uuid, instance)
        model = self._model.model_validate(obj, from_attributes=True)  # type: ignore
        return model

    async def remove(self, instance_uuid: UUID) -> UUID:
        odj: Mem = await self._repository.get(instance_uuid)
        status_code = await self._image_sever_service.del_from_s3(odj.image_key)
        if status_code == 200:
            obj_uuid = await self._repository.remove(instance_uuid)
        else:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"error deleting a file from storage. status_code={status_code}",
            )
        return obj_uuid


@lru_cache
def get_mem_service(
    repository: MemRepository = Depends(get_mem_repository),
    image_sever_service: ImageSaver = Depends(get_image_saver_service),
) -> MemService:
    return MemService(repository, image_sever_service, MemDB)
