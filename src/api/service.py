from fastapi import APIRouter, Depends

from src.models import Service
from src.schemas.service import ServiceBase, ServiceUpdate
from src.utils import *
from src.utils.auth import *

service_router = APIRouter(tags=["Service"], prefix="/service")


@service_router.post("/create")
async def create(
    service_item: ServiceBase,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    
    stmt = select(Service).where(Service.name == service_item.name)
    result = await service.db.execute(stmt)
    service_data = result.scalars().first()

    if service_data:
        raise HTTPException(
            # sherdan dovoetir
        )
    
    return await service.create(model=Service, db_obj=service_item)


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
