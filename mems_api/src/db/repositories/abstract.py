from abc import ABC, abstractmethod
from typing import TypeVar, Sequence, Any
from uuid import UUID
from src.db.entities.base import Entity

M = TypeVar("M", bound=Entity)


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self) -> Sequence[Any]:
        pass

    @abstractmethod
    async def get(self, instance_id: UUID) -> M | None:
        pass

    @abstractmethod
    async def create(self, instance) -> M:
        pass

    @abstractmethod
    async def update(self, instance_id: UUID, instance) -> M | None:
        pass

    @abstractmethod
    async def remove(self, instance_id: UUID) -> UUID:
        pass
