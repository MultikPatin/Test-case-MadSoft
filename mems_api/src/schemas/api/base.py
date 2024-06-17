from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    uuid: UUID = Field(
        description="UUID идентификатор",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )


class TimeMixin(BaseModel):
    created_at: datetime = Field(
        description="Дата создания записи",
        examples=["2024-04-19T17:17:31.711Z"],
    )
    updated_at: datetime = Field(
        description="Дата последнего редактирования записи",
        examples=["2024-04-19T19:17:31.711Z"],
    )


class ImageMixin(BaseModel):
    image_key: str | None = Field(
        description="Ключ для картинки в S3",
    )


class StringRepresent(BaseModel):
    code: HTTPStatus
    details: str
