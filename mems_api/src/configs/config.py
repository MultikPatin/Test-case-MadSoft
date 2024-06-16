from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings
from src.configs.postgres import PostgresSettings
from src.configs.s3_saver import S3Saver
from src.configs.sentry import SentrySettings
from src.configs.redis import RedisSettings
from src.configs.logger import LOGGING
from src.utils.settings import ServiceSettings

logging_config.dictConfig(LOGGING)


class AppSettings(ServiceSettings):
    name: str = Field(..., alias="API_NAME")
    description: str = Field(..., alias="API_DESCRIPTION")
    host: str = Field(..., alias="API_HOST")
    port: int = Field(..., alias="API_PORT")
    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()
    s3_sever: S3Saver = S3Saver()
    sentry: SentrySettings = SentrySettings()


settings = Settings()

if settings.app.debug:
    print(settings.model_dump())
