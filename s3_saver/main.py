import logging
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis

from src.configs.config import settings
from src.configs.logger import LOGGING
from src.endpoints.v1 import image


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    redis_limiter_connection = Redis(**settings.redis.connection_dict)
    await FastAPILimiter.init(redis_limiter_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    docs_url=settings.app.docs_url,
    openapi_url=settings.app.openapi_url,
    redoc_url=None,
    lifespan=lifespan,
)

app.include_router(
    image.router,
    prefix="/s3/v1/",
    tags=["image"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
