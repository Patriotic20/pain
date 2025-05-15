from fastapi import APIRouter
from src.schemas.lab import LabCreate , LabBase , LabUpdate
from src.utils.auth import *
from src.utils import *
from src.models import Lab , User



lab_router = APIRouter(
    tags=["Lab"],
    prefix="/lab"
)


@lab_router.post("/create")
async def create(
    lab_item: LabBase,
    current_user : User = Depends(RoleChecker("admin")),
    service : BaseService = Depends(get_base_service)
):
    lab_item = LabCreate(
        name=lab_item.name,
        description=lab_item.description,
        user_id=current_user.id
    )
    return await service.create(model=Lab , db_obj=lab_item)

@lab_router.get("/get_by_id/{lab_id}")
async def get_by_id( 
    lab_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.get_by_id(model=Lab , user_id=current_user.id , item_id=lab_id)

@lab_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.get_all(model=Lab , user_id=current_user.id)

@lab_router.put("/update/{lab_id}")
async def update(
    lab_id: int,
    lab_item: LabUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)

):
    return await service.update(model=Lab , item_id=lab_id, db_obj=lab_item , user_id=current_user.id)


@lab_router.delete("/delete/{lab_id}")
async def delete(
    lab_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.delete(model=Lab , item_id=lab_id , user_id = current_user.id)