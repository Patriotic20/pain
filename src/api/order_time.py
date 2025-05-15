from fastapi import APIRouter
from src.utils.auth import *
from src.utils import *
from src.models.order import OrderTime
from src.schemas.order_time import *

order_time_router = APIRouter(
    tags=["Order Time"],
    prefix="/order_time"
)



@order_time_router.post("/create")
async def create(
    order_time_item: OrderTimeBase,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    order_data = OrderTimeCreate(
        start_time=order_time_item.start_time,
        end_time=order_time_item.end_time,
        user_id=current_user.id
    )
    return await service.create(model=OrderTime , db_obj=order_data)

@order_time_router.get("/get_by_id/{order_time_id}")
async def get_by_id(
    order_time_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
    
):
    return await service.get_by_id(model=OrderTime , item_id=order_time_id , user_id=current_user.id)


@order_time_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.get_all(model=OrderTime , user_id=current_user.id)


@order_time_router.put("/update/{order_time_id}")
async def update(
    order_time_id: int,
    order_item: OrderTimeUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)
):
    return await service.update(model=OrderTime , db_obj=order_item , item_id=order_time_id , user_id=current_user.id)


@order_time_router.delete("/delete/{order_time_id}")
async def delete(
    order_time_id:int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service)

    ):
    return await service.delete(model=OrderTime , item_id=order_time_id , user_id=current_user.id)