from http import HTTPStatus

from pydantic import BaseModel


class StringRepresent(BaseModel):
    code: HTTPStatus
    details: str
