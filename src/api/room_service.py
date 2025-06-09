from fastapi import APIRouter, Depends
from src.models import *
from src.schemas.room_service import *
from src.utils import *
from src.utils.auth import *

room_service_router = APIRouter(tags=["Room service"], prefix="/room_service")


@room_service_router.post("/create")
async def create(
    room_service: RoomServiceCreate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    
    stmt = select(RoomService).where(RoomService.room_id == room_service.room_id , RoomService.service_id == room_service.service_id)
    result = await db.execute(stmt)
    room_service_exsiting = result.scalars().first()

    if room_service_exsiting:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room already assignment"
        )
    

    return await service.create(model=RoomService, db_obj=room_service)


@room_service_router.get("/get_by_id/{room_service_id}")
async def get_by_id(
    room_service_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.get_by_id(model=RoomService, item_id=room_service_id)


@room_service_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.get_all(model=RoomService)


@room_service_router.put("/update/{room_analis_id}")
async def update(
    room_service_id: int,
    room_analis: RoomServiceUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.update(
        model=RoomService, item_id=room_service_id, db_obj=room_analis
    )


@room_service_router.delete("/delete/{room_service_id}")
async def delete(
    room_service_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
):
    return await service.delete(model=RoomService, item_id=room_service_id)
