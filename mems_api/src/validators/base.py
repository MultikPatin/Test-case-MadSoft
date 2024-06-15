from typing import TypeVar, Generic
from uuid import UUID

from fastapi import HTTPException

from src.db.repositories.abstract import AbstractRepository

from src.validators.abstract import AbstractValidator, AbstractDuplicateNameMixin

R = TypeVar("R", bound=AbstractRepository)


class InitValidator(Generic[R]):
    _repository: R

    def __init__(self, repository: R):
        self._repository = repository


class BaseValidator(InitValidator[R], AbstractValidator):
    async def is_exists(self, instance_uuid: UUID) -> UUID:
        instance = await self._repository.get(instance_uuid)  # type: ignore
        if instance is None:
            raise HTTPException(status_code=404, detail="The object was not found")
        return instance_uuid


class DuplicateNameValidatorMixin(InitValidator[R], AbstractDuplicateNameMixin):
    async def is_duplicate_name(self, name: str) -> None:
        permission_uuid = await self._repository.get_uuid_by_name(name)  # type: ignore
        if permission_uuid is not None:
            raise HTTPException(
                status_code=400,
                detail="An object with that name already exists",
            )
