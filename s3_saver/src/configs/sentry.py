from pydantic import Field
from src.utils.settings import EnvSettings


class SentrySettings(EnvSettings):
    sentry_dsn: str = Field(..., alias="SENTRY_DSN")
