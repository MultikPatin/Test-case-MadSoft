from typing import Generic, TypeVar, Any, Sequence
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, func, select

from src.db.postgresdatabase import PostgresDatabase
from src.db.entities.base import Entity
from src.db.repositories.abstract import AbstractRepository

ModelType = TypeVar("ModelType", bound=Entity)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class InitRepository:
    _database: PostgresDatabase
    _model: ModelType  # type: ignore

    def __init__(self, database: PostgresDatabase, model: type[ModelType]):
        self._database = database
        self._model = model


class PostgresRepository(
    InitRepository,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
    AbstractRepository,
):
    async def create(self, instance: CreateSchemaType) -> ModelType:  # type: ignore
        async with self._database.get_session() as session:
            db_obj: ModelType = self._model(**instance.dict())  # type: ignore
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def get_all(self, **kwargs) -> Sequence[Any]:
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")
        async with self._database.get_session() as session:
            query = select(self._model).order_by(self._model.created_at.desc())  # type: ignore
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            db_obj = await session.execute(query)
            return db_obj.scalars().all()

    async def get(self, instance_uuid: UUID) -> ModelType | None:  # type: ignore
        async with self._database.get_session() as session:
            db_obj: Any = await session.execute(
                select(self._model).filter_by(uuid=instance_uuid)
            )
            return db_obj.scalars().first()

    async def update(  # type: ignore
        self, instance_uuid: UUID, instance: UpdateSchemaType
    ) -> ModelType | None:
        async with self._database.get_session() as session:
            db_obj: ModelType | None = await self.get(instance_uuid)

            obj_data = jsonable_encoder(db_obj)
            update_data = instance.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def remove(self, instance_uuid: UUID) -> UUID:
        async with self._database.get_session() as session:
            await session.execute(delete(self._model).filter_by(uuid=instance_uuid))
            await session.commit()
            return instance_uuid

    async def count(self, **kwargs) -> int | None:
        async with self._database.get_session() as session:
            db_obj: Any = await session.execute(
                select(func.count()).select_from(self._model).filter_by(**kwargs)
            )
            return db_obj.scalars().first()


class NameFieldRepositoryMixin(InitRepository):
    async def get_by_name(self, name: str) -> ModelType | None:
        async with self._database.get_session() as session:
            db_obj: Any = await session.execute(
                select(self._model).filter_by(name=name)
            )
            return db_obj.scalars().first()
