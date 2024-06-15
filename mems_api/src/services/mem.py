from functools import lru_cache

from fastapi import Depends

from src.schemas.api.v1.mem import (
    RequestMemCreate,
    RequestMemUpdate,
    ResponseMemPaginated,
)
from src.schemas.db.mem import MemDB
from src.services.base import BaseService
from src.db.repositories.mem import (
    MemRepository,
    get_mem_repository,
)


class MemService(
    BaseService[
        MemDB,
        ResponseMemPaginated,
        RequestMemCreate,
        RequestMemUpdate,
    ]
):
    pass


@lru_cache
def get_mem_service(
    repository: MemRepository = Depends(get_mem_repository),
) -> MemService:
    return MemService(repository, MemDB)
