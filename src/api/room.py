from fastapi import APIRouter
from src.utils.auth import *
from src.utils import *
from src.models import *
from src.schemas.room import RoomBase , RoomCreate , RoomUpdate

room_router = APIRouter(
    tags=["Room"],
    prefix="/room"
)



@room_router.post("/create")
async def create(
    analis_item: RoomBase,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserLab.lab_id).where(UserLab.user_id == current_user.id)
    result = await db.execute(query)
    lab_id = result.scalars().first()

    room_data = RoomCreate(
        name=analis_item.name,
        lab_id=lab_id,
        description=analis_item.description,
        start_time=analis_item.start_time,
        end_time=analis_item.end_time 
    )
    return await service.create(model=Room , db_obj=room_data)
    

@room_router.get("/get_by_id/{room_id}")
async def get_by_id(
    room_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserLab.lab_id).where(UserLab.user_id == current_user.id)
    result = await db.execute(query)
    lab_id = result.scalars().first()
    return await service.get_by_id(model=Room , item_id=room_id , filter_field="lab_id" , filter_value=lab_id)

@room_router.get("/get_all")
async def get_by_id(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserLab.lab_id).where(UserLab.user_id == current_user.id)
    result = await db.execute(query)
    lab_id = result.scalars().first()

    return await service.get_all(model=Room , filter_field="lab_id", filter_value=lab_id)
    


@room_router.put("/update/{room_id}")
async def update(
    room_id: int,
    room_item: RoomUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserLab.lab_id).where(UserLab.user_id == current_user.id)
    result = await db.execute(query)
    lab_id = result.scalars().first()

    return await service.update(model=Room , db_obj=room_item , item_id=room_id , filter_field="lab_id" , filter_value=lab_id)

@room_router.delete("/delete/{room_id}")
async def get_by_id(
    room_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db)
):
    query = select(UserLab.lab_id).where(UserLab.user_id == current_user.id)
    result = await db.execute(query)
    lab_id = result.scalars().first()

    return await service.delete(model=Room , item_id=room_id , filter_field="lab_id" , filter_value=lab_id)
