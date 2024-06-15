from typing import Annotated
from uuid import UUID

from fastapi import Depends, Path

from src.validators.base import BaseValidator, DuplicateNameValidatorMixin
from src.db.entities.mem import Mem
from src.db.repositories.mem import (
    MemRepository,
    get_mem_repository,
)


class MemValidator(
    BaseValidator[MemRepository, Mem], DuplicateNameValidatorMixin
):
    pass


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
