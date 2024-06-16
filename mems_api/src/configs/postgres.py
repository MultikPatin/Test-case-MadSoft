from pydantic import SecretStr
from pydantic.fields import Field

from src.utils.sqlalchemy import SQLAlchemyConnectMixin


class PostgresSettings(SQLAlchemyConnectMixin):
    """
    This class is used to store the Postgres db connection settings.
    """

    database: str = Field(..., alias="POSTGRES_DB")
    user: str = Field(..., alias="POSTGRES_USER")
    password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    host: str = Field(..., alias="POSTGRES_HOST")
    port: int = Field(..., alias="POSTGRES_PORT")
    host_local: str = Field(..., alias="POSTGRES_HOST_LOCAL")
    port_local: int = Field(..., alias="POSTGRES_PORT_LOCAL")


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()
