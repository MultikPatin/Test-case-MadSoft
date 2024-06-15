from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.api.base import StringRepresent
from src.schemas.api.v1.mem import (
    RequestMemCreate,
    RequestMemUpdate,
    ResponseMem,
    ResponseMemsPaginated,
)
from src.services.mem import MemService, get_mem_service

from src.validators.mem import mem_uuid_annotation, MemValidator, get_mem_validator

router = APIRouter()


@router.get(
    "/",
    response_model=ResponseMemsPaginated,
    summary="Get a list of roles",
)
async def get_mems(
    mem_service: MemService = Depends(get_mem_service),
) -> ResponseMemsPaginated:
    mems = await mem_service.get_all()
    if not mems:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="mems not found")
    return [
        ResponseMem(
            uuid=mem.uuid,
            name=mem.name,
        )
        for mem in mems
    ]


@router.get(
    "/{mem_uuid}/",
    response_model=ResponseMem,
    response_model_exclude_none=True,
    summary="Get a mem details by uuid",
)
async def get_mem(
    mem_uuid: mem_uuid_annotation,
    mem_service: MemService = Depends(get_mem_service),
) -> ResponseMem:
    mem = await mem_service.get(mem_uuid)
    if not mem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="mem not found")
    return mem


@router.post(
    "/",
    response_model=ResponseMem,
    response_model_exclude_none=True,
    summary="Create a mem",
)
async def create_mem(
    body: RequestMemCreate,
    mem_service: MemService = Depends(get_mem_service),
    mem_validator: MemValidator = Depends(get_mem_validator),
) -> ResponseMem:
    await mem_validator.is_duplicate_name(body.name)
    mem = await mem_service.create(body)
    return mem


@router.patch(
    "/{mem_uuid}/",
    response_model=ResponseMem,
    response_model_exclude_none=True,
    summary="Change the mem by uuid",
)
async def update_mem(
    mem_uuid: mem_uuid_annotation,
    body: RequestMemUpdate,
    mem_service: MemService = Depends(get_mem_service),
    mem_validator: MemValidator = Depends(get_mem_validator),
) -> ResponseMem:
    mem = await mem_service.update(await mem_validator.is_exists(mem_uuid), body)
    return mem


@router.delete(
    "/{mem_uuid}/",
    response_model=StringRepresent,
    summary="Delete the mem by uuid",
)
async def remove_mem(
    mem_uuid: mem_uuid_annotation,
    mem_service: MemService = Depends(get_mem_service),
    mem_validator: MemValidator = Depends(get_mem_validator),
) -> StringRepresent:
    await mem_service.remove(await mem_validator.is_exists(mem_uuid))
    return StringRepresent(code=HTTPStatus.OK, details="Mem deleted successfully")
