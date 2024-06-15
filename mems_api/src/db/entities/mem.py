from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.entities.base import Entity

# if TYPE_CHECKING:
#     from src.db.entities.mem import Mem


class Mem(Entity):
    __tablename__ = "mems"

    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))

    # user: Mapped[list["User"] | None] = relationship(
    #     "User",
    #     back_populates="role",
    #     order_by="User.uuid.desc()",
    # )
    # permissions = relationship(
    #     "Permission",
    #     cascade="all, delete",
    #     secondary="roles_permissions",
    #     back_populates="roles",
    # )
