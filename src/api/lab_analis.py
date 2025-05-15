from fastapi import APIRouter , Depends
from src.models import User  , LabAnalis
from src.utils.auth import *
from src.schemas.lab_analis import *
from src.utils import *

lab_analis_router = APIRouter(
    tags=["Lab analis"],
    prefix="/lab_analis"
)


@lab_analis_router.post("/create")
async def create(
    lab_items: LabAnalisCreate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.create(model=LabAnalis , db_obj=lab_items)

@lab_analis_router.get("/get_by_id/{lab_anslis_id}")
async def get_by_id(
    lab_anslis_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.get_by_id(model=LabAnalis , item_id=lab_anslis_id)

@lab_analis_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.get_all(model=LabAnalis)


@lab_analis_router.put("/update/{lab_analis_id}")
async def update(
    lab_analis_id: int,
    lab_analis: LabAnalisUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.update(model=LabAnalis , item_id=lab_analis_id , db_obj=lab_analis)

@lab_analis_router.delete("/delete/{lab_analis_id}")
async def delete(
    lab_analis_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.delete(model=LabAnalis , item_id=lab_analis_id)
