from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_limiter.depends import RateLimiter

from src.schemas.api.base import StringRepresent

from src.schemas.api.v1.image import RequestPutImage, ResponsePutImage
from src.services.imsge import get_image_service, ImageService
from src.validators.image import is_exists

router = APIRouter()


@router.put(
    "/",
    response_model=ResponsePutImage,
    response_model_exclude_none=True,
    summary="Put the image to S3",
    dependencies=[Depends(RateLimiter(times=5, seconds=1))],
)
async def put_image(
    body: RequestPutImage,
    mem_service: ImageService = Depends(get_image_service),
) -> ResponsePutImage:
    """
    This method is responsible for uploading an image to S3.

    Args:
    - **body** (`RequestPutImage`): The request body containing the file name of the image to be uploaded.
    Returns:

    - **ResponsePutImage**: The response containing the image URL and key.

    Raises:
    - **Exception**: If an error occurs while uploading the image.
    """
    file_name = await is_exists(body.file_name)
    data = await mem_service.put(file_name)
    return ResponsePutImage(
        image_url=data.image_url,
        image_key=data.image_key,
    )


@router.delete(
    "/{image_key}/",
    response_model=StringRepresent,
    summary="Delete the image from S3",
)
async def remove_image(
    image_key: Annotated[
        str,
        Query(
            min_length=1,
            description="ключ файла в S3 хранилище",
            example="cscs3vv02mmsom",
        ),
    ],
    mem_service: ImageService = Depends(get_image_service),
) -> StringRepresent:
    """
    This method is responsible for deleting an image from S3.

    Args:
    - **image_key** (`str`): The unique identifier of the image to be deleted.
    Returns:
    - **StringRepresent**: A response containing the HTTP status code and a message indicating the success of the image deletion.

    Raises:
    - **Exception**: If an error occurs while deleting the image.
    """
    file_key = await mem_service.remove(image_key)
    return StringRepresent(
        code=HTTPStatus.OK, details=f"Image {file_key} deleted successfully"
    )
