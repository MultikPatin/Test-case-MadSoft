from typing import Generic, TypeVar, Any
from uuid import UUID

from pydantic import BaseModel

from src.db.repositories.abstract import AbstractRepository

DBSchemaType = TypeVar("DBSchemaType", bound=BaseModel)
DBSchemaPaginationType = TypeVar("DBSchemaPaginationType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class InitService:
    _model: DBSchemaType  # type: ignore

    def __init__(self, repository: AbstractRepository, model: type[DBSchemaType]):
        self._repository = repository
        self._model = model


class BaseService(
    InitService,
    Generic[DBSchemaType, DBSchemaPaginationType, CreateSchemaType, UpdateSchemaType],
):
    async def get(self, instance_uuid: UUID) -> DBSchemaType | None:
        obj: Any = await self._repository.get(instance_uuid)
        if obj is None:
            return None
        model = self._model.model_validate(obj, from_attributes=True)  # type: ignore
        return model

    async def get_all(self, **kwargs) -> list[DBSchemaType] | None:
        objs: Any = await self._repository.get_all(**kwargs)
        if objs is None:
            return None
        models = [self._model.model_validate(obj, from_attributes=True) for obj in objs]  # type: ignore
        return models

    async def create(self, instance: CreateSchemaType) -> DBSchemaType:
        obj: Any = await self._repository.create(instance)
        model = self._model.model_validate(obj, from_attributes=True)  # type: ignore
        return model

    async def update(
        self, instance_uuid: UUID, instance: UpdateSchemaType
    ) -> DBSchemaType:
        obj: Any = await self._repository.update(instance_uuid, instance)
        model = self._model.model_validate(obj, from_attributes=True)  # type: ignore
        return model

    async def remove(self, instance_uuid: UUID) -> UUID:
        obj_uuid = await self._repository.remove(instance_uuid)
        return obj_uuid

    async def count(self) -> int | None:
        count = await self._repository.count()
        return count
