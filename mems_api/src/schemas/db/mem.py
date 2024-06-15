from src.schemas.db.base import BaseMixin


class MemDB(BaseMixin):
    name: str
    description: str | None
    image_url: str
