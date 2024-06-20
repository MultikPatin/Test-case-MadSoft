from abc import ABC, abstractmethod
from typing import TypeVar, Sequence, Any
from uuid import UUID
from src.db.entities.base import Entity

ModelType = TypeVar("ModelType", bound=Entity)


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self, **kwargs) -> Sequence[Any]:
        pass

    @abstractmethod
    async def get(self, instance_id: UUID) -> ModelType | None:
        pass

    @abstractmethod
    async def create(self, instance) -> ModelType:
        pass

    @abstractmethod
    async def update(self, instance_id: UUID, instance) -> ModelType | None:
        pass

    @abstractmethod
    async def remove(self, instance_id: UUID) -> UUID:
        pass

    @abstractmethod
    async def count(self, **kwargs) -> int | None:
        pass
