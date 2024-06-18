from pydantic import SecretStr
from pydantic.fields import Field

from src.utils.sqlalchemy import SQLAlchemyConnectMixin


class PostgresSettings(SQLAlchemyConnectMixin):
    """
    This class is used to store the Postgres db connection settings.
    """

    database: str = Field("db_mems", alias="POSTGRES_DB")
    user: str = Field("app", alias="POSTGRES_USER")
    password: SecretStr = Field("123qwe", alias="POSTGRES_PASSWORD")
    host: str = Field("postgres", alias="POSTGRES_HOST")
    port: int = Field(5432, alias="POSTGRES_PORT")
    host_local: str = Field("localhost", alias="POSTGRES_HOST_LOCAL")
    port_local: int = Field(5432, alias="POSTGRES_PORT_LOCAL")


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()
