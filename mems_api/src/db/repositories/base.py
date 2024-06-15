from typing import Generic, TypeVar, Any, Sequence
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, func, select

from src.db.postgresdatabase import PostgresDatabase
from src.db.entities.base import Entity
from src.db.repositories.abstract import AbstractRepository

M = TypeVar("M", bound=Entity)
C = TypeVar("C", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)


class InitRepository:
    _database: PostgresDatabase
    _model: M

    def __init__(self, database: PostgresDatabase, model: type[M]):
        self._database = database
        self._model = model


class PostgresRepository(
    InitRepository,
    Generic[M, C, U],
    AbstractRepository,
):
    async def create(self, instance: C) -> M:
        async with self._database.get_session() as session:
            db_obj = self._model(**instance.dict())
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def get_all(self) -> Sequence[Any]:
        async with self._database.get_session() as session:
            db_objs: Any = await session.execute(select(self._model))
            return db_objs.scalars().all()

    async def get(self, instance_uuid: UUID) -> M | None:
        async with self._database.get_session() as session:
            db_obj: Any = await session.execute(
                select(self._model).filter_by(uuid=instance_uuid)
            )
            return db_obj.scalars().first()

    async def update(self, instance_uuid: UUID, instance: U) -> M | None:
        async with self._database.get_session() as session:
            db_obj: M | None = await self.get(instance_uuid)

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


class NameFieldRepositoryMixin(InitRepository):
    async def get_by_name(self, name: str) -> M | None:
        async with self._database.get_session() as session:
            db_obj: Any = await session.execute(
                select(self._model).filter_by(name=name)
            )
            return db_obj.scalars().first()


class CountRepositoryMixin(InitRepository):
    async def count(self) -> int | None:
        async with self._database.get_session() as session:
            db_obj = await session.execute(
                select(func.count()).select_from(self._model)
            )
            return db_obj.scalars().first()
