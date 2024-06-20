from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.entities.base import Entity


class Mem(Entity):
    __tablename__ = "mems"

    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))
    image_url: Mapped[str] = mapped_column(String(255))
    image_key: Mapped[str | None] = mapped_column(String(255))
