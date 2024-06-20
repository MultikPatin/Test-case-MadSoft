from pydantic import BaseModel, Field


class RequestPutImage(BaseModel):
    file_name: str = Field(
        description="Имя файла для загрузки в S3 из директории статики",
        examples=["exemple.jpg"],
    )


class ResponsePutImage(BaseModel):
    image_url: str = Field(
        description="URL картинки в S3 хранилище",
        examples=["https://s3/exemple.jpg"],
    )
    image_key: str = Field(
        description="Ключ картинки в S3 хранилище",
        examples=["cscs33csc2r0cs"],
    )
