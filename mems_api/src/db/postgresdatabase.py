import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.configs.postgres import PostgresSettings, get_postgres_settings

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class PostgresDatabase:
    def __init__(self, settings: PostgresSettings) -> None:
        self._async_session_factory = async_sessionmaker(
            create_async_engine(
                settings.postgres_connection_url, echo=settings.sqlalchemy_echo
            )
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        session: AsyncSession = AsyncSession()
        try:
            logger.debug("==> Session open")
            session = self._async_session_factory()
            yield session
        except Exception as error:
            logger.exception("==> Session rollback because of exception", error)
            await session.rollback()
            raise
        finally:
            logger.debug("==> Session close")
            await session.close()


def get_postgres_auth_db(
    settings: PostgresSettings = Depends(get_postgres_settings),
) -> PostgresDatabase:
    return PostgresDatabase(settings)
