from abc import ABC, abstractmethod
from uuid import UUID


class AbstractValidator(ABC):
    @abstractmethod
    async def is_exists(self, instance_uuid: UUID) -> UUID:
        pass


class AbstractDuplicateNameMixin(ABC):
    @abstractmethod
    async def is_duplicate_name(self, name: str) -> None:
        pass
