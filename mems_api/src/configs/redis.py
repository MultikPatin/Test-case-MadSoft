from typing import Any

from pydantic import Field

from src.utils.settings import ServiceSettings


class RedisSettings(ServiceSettings):
    """
    This class is used to store the REDIS connection settings.
    """

    host: str = Field("redis", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")
    host_local: str = Field("localhost", alias="REDIS_HOST_LOCAL")
    port_local: int = Field(6379, alias="REDIS_PORT_LOCAL")

    @property
    def connection_dict(self) -> dict[str, Any]:
        return {
            "host": self.correct_host(),
            "port": self.correct_port(),
        }
