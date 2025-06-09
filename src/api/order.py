
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import *
from src.schemas.order import OrderBase
from src.utils import *
from src.utils.auth import *

order_router = APIRouter(tags=["Order"], prefix="/order")


@order_router.post("/create")
async def create(
    order_input: OrderBase,
    current_user: User = Depends(RoleChecker("admin")),
    db: AsyncSession = Depends(get_db),
):
    # Step 1: Verify that room_service_id exists in room_services
    stmt = select(RoomService).where(RoomService.id == order_input.room_service_id)
    result = await db.execute(stmt)
    room_service = result.scalar_one_or_none()

    if room_service is None:
        raise HTTPException(
            status_code=400,
            detail="The provided room_service_id does not exist"
        )

    # Step 2: Get the room_id associated with this room_service
    room_id = room_service.room_id

    # Step 3: Select time slots for the associated room_id
    stmt = select(TimeSlot.id).where(TimeSlot.room_id == room_id)
    result = await db.execute(stmt)
    time_slot_ids = result.scalars().all()

    if not time_slot_ids:
        raise HTTPException(
            status_code=404,
            detail="No time slots found for the room associated with this room service"
        )

    # Step 4: Create orders with the validated room_service_id and corresponding time_slot_ids
    orders_to_create = [
        Order(
            room_service_id=order_input.room_service_id,
            time_slot_id=time_slot_id,
            discount=order_input.discount
        )
        for time_slot_id in time_slot_ids
    ]

    if orders_to_create:
        db.add_all(orders_to_create)
        await db.commit()
        for order in orders_to_create:
            await db.refresh(order)

    return orders_to_create

@order_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_all(model=Order)


@order_router.get("/get_by_id/{order_id}")
async def get_by_id(
    order_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.get_by_id(model=Order , item_id=order_id)

