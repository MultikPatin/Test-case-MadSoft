from pydantic import Field
from src.utils.settings import EnvSettings


class S3Saver(EnvSettings):
    host: str = Field(..., alias="S3_SAVER_HOST")
    port: int = Field(..., alias="S3_SAVER_PORT")

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/api/v1/s3/images"
