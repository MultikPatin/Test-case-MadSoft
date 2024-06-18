from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from src.schemas.api.base import StringRepresent
from src.schemas.api.v1.mem import (
    ResponseMem,
    RequestMemCreate,
    MemCreate,
)
from src.services.mem import MemService, get_mem_service

from src.validators.mem import mem_uuid_annotation, MemValidator, get_mem_validator

router = APIRouter()


@router.put(
    "/",
    response_model=ResponseMem,
    response_model_exclude_none=True,
    summary="Put the image to S3",
    dependencies=[Depends(RateLimiter(times=5, seconds=1))],
)
async def put_image(
        body: RequestMemCreate,
        mem_service: MemService = Depends(get_mem_service),
        mem_validator: MemValidator = Depends(get_mem_validator),
) -> ResponseMem:
    await mem_validator.is_duplicate_name(body.name)
    instance = MemCreate(
        name=body.name,
        description=body.description,
        image_url=body.image_url,
        image_key=None,
    )
    mem = await mem_service.create(instance)
    return ResponseMem(
        uuid=mem.uuid,
        created_at=mem.created_at,
        updated_at=mem.updated_at,
        name=mem.name,
        description=mem.description,
        image_url=mem.image_url,
    )


@router.delete(
    "/{image_key}/",
    response_model=StringRepresent,
    summary="Delete the image from S3",
)
async def remove_image(
        mem_uuid: mem_uuid_annotation,
        mem_service: MemService = Depends(get_mem_service),
        mem_validator: MemValidator = Depends(get_mem_validator),
) -> StringRepresent:
    await mem_service.remove(await mem_validator.is_exists(mem_uuid))
    return StringRepresent(code=HTTPStatus.OK, details="Mem deleted successfully")
