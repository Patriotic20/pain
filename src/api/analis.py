from fastapi import APIRouter, Depends
from src.models import User , Analysis 
from src.schemas.analis import AnalisBase , AnalisResponse, AnalisUpdate
from src.utils.auth import *
from src.utils import *


analis_router = APIRouter(
    tags=["Analis"],
    prefix="/analis"
)


@analis_router.post("/create")
async def create(
    analis_item: AnalisBase,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.create(model=Analysis , db_obj=analis_item)


@analis_router.get("/get_by_id/{analis_id}")
async def get_by_id(
    analis_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.get_by_id(model=Analysis, item_id=analis_id)

@analis_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.get_all(model=Analysis)


@analis_router.put("/update/{analis_id}")
async def update(
    analis_id: int,
    analis_item: AnalisUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.update(model=Analysis , item_id=analis_id , db_obj=analis_item)


@analis_router.delete("/delete/{analis_id}")
async def delete(
    analis_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.delete(model=Analysis , item_id=analis_id)