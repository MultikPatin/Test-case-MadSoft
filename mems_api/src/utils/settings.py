import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ServiceSettings(EnvSettings):
    host: str = ""
    port: int = 0
    host_local: str = ""
    port_local: int = 0
    local: bool = Field(..., alias="LOCAL") == "True"
    debug: bool = Field(..., alias="DEBUG") == "True"

    def correct_host(self) -> str:
        if self.local:
            return self.host_local
        return self.host

    def correct_port(self) -> int:
        if self.local:
            return self.port_local
        return self.port

