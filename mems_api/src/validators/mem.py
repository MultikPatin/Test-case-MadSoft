from typing import Annotated
from uuid import UUID
from fastapi import Depends, Path
from functools import lru_cache
from src.db.repositories.mem import (
    MemRepository,
    get_mem_repository,
)
from src.validators.base import BaseValidator, DuplicateNameValidatorMixin


class MemValidator(
    BaseValidator[MemRepository], DuplicateNameValidatorMixin[MemRepository]
):
    pass


@lru_cache
def get_mem_validator(
    repository: MemRepository = Depends(get_mem_repository),
) -> MemValidator:
    return MemValidator(repository)


mem_uuid_annotation = Annotated[
    UUID,
    Path(
        alias="mem_uuid",
        title="mem uuid",
        description="The UUID of the mem",
        example="6a0a479b-cfec-41ac-b520-41b2b007b611",
    ),
]
