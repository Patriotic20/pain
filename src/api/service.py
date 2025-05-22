from fastapi import APIRouter, Depends
from src.models import Service
from src.schemas.service import ServiceBase , ServiceUpdate
from src.utils.auth import *
from src.utils import *


service_router = APIRouter(tags=["Analis"], prefix="/analis")


@service_router.post("/create")
async def create(
    analis_item: ServiceBase,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.create(model=Service, db_obj=analis_item)


@service_router.get("/get_by_id/{analis_id}")
async def get_by_id(
    analis_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.get_by_id(model=Service, item_id=analis_id)


@service_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.get_all(model=Service)


@service_router.put("/update/{analis_id}")
async def update(
    analis_id: int,
    analis_item: ServiceUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.update(model=Service, item_id=analis_id, db_obj=analis_item)


@service_router.delete("/delete/{analis_id}")
async def delete(
    analis_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.delete(model=Service, item_id=analis_id)
