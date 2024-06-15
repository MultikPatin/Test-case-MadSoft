from functools import lru_cache

from fastapi import Depends

from src.schemas.api.v1.mem import (
    RequestMemCreate,
    RequestMemUpdate,
)
from src.db.postgresdatabase import (
    PostgresDatabase,
    get_postgres_auth_db,
)
from src.db.entities.mem import Mem
from src.db.repositories.base import (
    CountRepositoryMixin,
    NameFieldRepositoryMixin,
    PostgresRepository,
)


class MemRepository(
    PostgresRepository[
        Mem,
        RequestMemCreate,
        RequestMemUpdate,
    ],
    NameFieldRepositoryMixin,
    CountRepositoryMixin,
):
    pass


@lru_cache
def get_mem_repository(
    database: PostgresDatabase = Depends(get_postgres_auth_db),
) -> MemRepository:
    return MemRepository(database, Mem)
