from pydantic import BaseModel, Field

from src.schemas.api.base import (
    TimeMixin,
    UUIDMixin,
)
from src.utils.pagination import PaginatedMixin


class RequestMemUpdate(BaseModel):
    description: str = Field(
        description="Описание мема",
        example="Супер смешной!)",
        min_length=1,
        max_length=255,
    )


class RequestMemCreate(RequestMemUpdate):
    description: str | None = Field(
        description="Описание мема",
        example="Супер смешной!)",
        min_length=1,
        max_length=255,
    )
    name: str = Field(
        description="Наименование мема",
        example="Язь",
        min_length=1,
        max_length=64,
    )


class MemBase(RequestMemUpdate, UUIDMixin, TimeMixin):
    name: str = Field(
        description="Наименование мема",
        example="Язь",
        min_length=1,
        max_length=64,
    )


class ResponseMem(MemBase, UUIDMixin, TimeMixin):
    pass


class ResponseMemPaginated(PaginatedMixin):
    mems: list[ResponseMem]
