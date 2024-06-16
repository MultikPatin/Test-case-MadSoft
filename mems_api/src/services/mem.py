from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

from src.schemas.api.v1.mem import (
    RequestMemCreate,
    RequestMemUpdate,
    ResponseMemPaginated,
)
from src.schemas.db.mem import MemDB
from src.services.base import BaseService
from src.db.repositories.mem import (
    MemRepository,
    get_mem_repository,
)
from src.services.imsge_saver import ImageSaver, get_image_sever_service


class MemService(
    BaseService[
        MemDB,
        ResponseMemPaginated,
        RequestMemCreate,
        RequestMemUpdate,
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

    async def create(self, instance: RequestMemCreate) -> MemDB:
        obj: Any = await self._repository.create(instance)
        model = self._model.model_validate(obj, from_attributes=True)  # type: ignore
        return model

    async def update(self, instance_uuid: UUID, instance: RequestMemUpdate) -> MemDB:
        obj: Any = await self._repository.update(instance_uuid, instance)
        model = self._model.model_validate(obj, from_attributes=True)  # type: ignore
        return model

    async def remove(self, instance_uuid: UUID) -> UUID:
        obj_uuid = await self._repository.remove(instance_uuid)
        return obj_uuid


@lru_cache
def get_mem_service(
    repository: MemRepository = Depends(get_mem_repository),
    image_sever_service: ImageSaver = Depends(get_image_sever_service),
) -> MemService:
    return MemService(repository, image_sever_service, MemDB)
