import os
from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings
from src.configs.sentry import SentrySettings
from src.configs.redis import RedisSettings
from src.configs.logger import LOGGING
from src.utils.settings import ServiceSettings, EnvSettings

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AppSettings(ServiceSettings):
    name: str = Field(..., alias="API_NAME")
    description: str = Field(..., alias="API_DESCRIPTION")
    host: str = Field("s3_saver", alias="API_HOST")
    port: int = Field(8080, alias="API_PORT")
    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")
    base_dir: str = BASE_DIR


class StaticSettings(EnvSettings):
    main_dir: str = Field(..., alias="STATIC_MAIN_DIR")
    mem_images_dir: str = Field(..., alias="STATIC_MEM_IMAGES_DIR")


class S3Settings(EnvSettings):
    access_key: str = Field(..., alias="S3_ACCESS_KEY")
    secret_key: str = Field(..., alias="S3_SECRET_KEY")
    endpoint_url: str = Field(..., alias="S3_ENDPOINT_URL")
    bucket_name: str = Field(..., alias="S3_BUCKET_NAME")


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    s3: S3Settings = S3Settings()
    static: StaticSettings = StaticSettings()
    redis: RedisSettings = RedisSettings()
    sentry: SentrySettings = SentrySettings()


settings = Settings()

if settings.app.debug:
    print(settings.model_dump())
