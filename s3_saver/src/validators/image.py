from http import HTTPStatus
import os

from fastapi import HTTPException
from src.configs.config import settings


async def is_exists(file_name: str) -> str:
    file_dir_path = os.path.join(
        settings.static.main_dir, settings.static.mem_images_dir
    )
    file_path = os.path.join(str(file_dir_path), file_name)

    try:
        with open(file_path, "r") as f:
            f.read()
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="The object was not found"
        )
    return file_name
