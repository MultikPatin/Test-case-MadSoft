from pydantic import BaseModel, Field

from src.schemas.api.base import (
    TimeMixin,
    UUIDMixin,
    ImageMixin,
)
from src.utils.pagination import PaginatedMixin


class RequestMemUpdate(BaseModel):
    image_url: str = Field(
        description="Путь до загруженной картинки",
        examples=["static/exemple.jpg"],
    )
    description: str | None = Field(
        description="Описание мема",
        examples=["Супер смешной!)"],
        min_length=1,
        max_length=255,
    )


class MemUpdate(RequestMemUpdate, ImageMixin):
    pass


class RequestMemCreate(RequestMemUpdate):
    description: str | None = Field(
        description="Описание мема",
        examples=["Супер смешной!)"],
        min_length=1,
        max_length=255,
    )
    name: str = Field(
        description="Наименование мема",
        examples=["Язь"],
        min_length=1,
        max_length=64,
    )


class MemCreate(RequestMemCreate, ImageMixin):
    pass


class MemBase(UUIDMixin, TimeMixin):
    description: str | None = Field(
        description="Описание мема",
        examples=["Супер смешной!)"],
        min_length=1,
        max_length=255,
    )
    name: str = Field(
        description="Наименование мема",
        examples=["Язь"],
        min_length=1,
        max_length=64,
    )
    image_url: str = Field(
        description="URL картинки",
        examples=["https://image.png"],
        min_length=1,
        max_length=64,
    )


class ResponseMem(MemBase, UUIDMixin, TimeMixin):
    pass


class ResponseMemPaginated(PaginatedMixin):
    mems: list[ResponseMem]
