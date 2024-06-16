from typing import Annotated

from fastapi import HTTPException, UploadFile, File


async def validate_image_size(file) -> None:
    file.file.seek(0, 2)
    file_size = file.file.tell()
    print(file_size)
    await file.seek(0)

    if file_size > 10 * 10:
        raise HTTPException(status_code=400, detail="File too large")


image_annotation = Annotated[
    UploadFile,
    File(
        alias="image_file",
        title="image file",
        description="The image file for the mem",
        media_type="image/*",
        is_required=True,
    ),
]
