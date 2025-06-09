from fastapi import APIRouter

from src.models import *
from src.schemas.room import RoomBase, RoomCreate, RoomUpdate
from src.utils import *
from src.utils.auth import *

room_router = APIRouter(tags=["Room"], prefix="/room")


@room_router.post("/create")
async def create(
    analis_item: RoomCreate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    
    stmt = select(Room).where(Room.name == analis_item.name , Room.lab_id == analis_item.lab_id)
    result = await db.execute(stmt)
    room_data = result.scalars().first()

    if room_data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This {room_data.name} room already create"
        )

    return await service.create(model=Room, db_obj=analis_item)


@room_router.get("/get_by_id/{room_id}")
async def get_by_id(
    room_id: int,
    lab_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_by_id(
        model=Room, item_id=room_id, filter_field="lab_id", filter_value=lab_id
    )


@room_router.get("/get_all")
async def get_by_id(
    lab_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    lab_result = await db.execute(select(Lab).where(Lab.id == lab_id))
    lab_info = lab_result.scalars().first()

    if not lab_info:
        raise HTTPException(status_code=404, detail="Lab not found")

    rooms = await service.get_all(model=Room, filter_field="lab_id", filter_value=lab_id)

    formatted_rooms = [
        {
            "id": room.id,
            "name": room.name,
            "description": room.description,
            "start_time": room.start_time,
            "end_time": room.end_time
        }
        for room in rooms
    ]

    # Structure the response
    response = {
        "lab_id": lab_info.id,
        "lab_name": lab_info.name,
        "rooms": formatted_rooms
    }
    return response


@room_router.put("/update/{room_id}")
async def update(
    room_id: int,
    room_item: RoomUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    query = select(UserLab.lab_id).where(UserLab.user_id == current_user.id)
    result = await db.execute(query)
    lab_id = result.scalars().first()

    return await service.update(
        model=Room,
        db_obj=room_item,
        item_id=room_id,
        filter_field="lab_id",
        filter_value=lab_id,
    )


@room_router.delete("/delete/{room_id}")
async def get_by_id(
    room_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    query = select(UserLab.lab_id).where(UserLab.user_id == current_user.id)
    result = await db.execute(query)
    lab_id = result.scalars().first()

    return await service.delete(
        model=Room, item_id=room_id, filter_field="lab_id", filter_value=lab_id
    )
