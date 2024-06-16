from typing import Annotated

from fastapi import HTTPException, UploadFile, File

VALID_CONTENT_TYPES = [
    "image/jpeg",
    "image/png",
    "image/bmp",
]


async def is_valid_image_size(file) -> None:
    file.file.seek(0, 2)
    file_size = file.file.tell()
    print(file_size)
    await file.seek(0)

    if file_size > 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")


async def is_valid_image_type(file) -> None:
    content_type = file.content_type
    if content_type not in VALID_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")


image_annotation = Annotated[
    UploadFile,
    File(
        description="The image file for the mem",
    ),
]
