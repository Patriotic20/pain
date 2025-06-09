from fastapi import APIRouter, Depends, HTTPException

from src.models import Room, TimeSlot, UserLab
from src.utils import *
from src.utils.auth import *
from src.utils.time_utils import _generate_ranges, time_string_to_float

time_slot_router = APIRouter(tags=["Time slots"], prefix="/time_slots")


@time_slot_router.post("/create")
async def create(
    room_id: int,
    interval_time: float,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    try:

        stmt = await db.execute(
            select(Room)
            .join(UserLab, UserLab.lab_id == Room.lab_id)
            .where(UserLab.user_id == current_user.id)
            .where(Room.id == room_id)
        )

        room_data = stmt.scalars().first()

        start_time = time_string_to_float(time_str=room_data.start_time)
        end_time = time_string_to_float(time_str=room_data.end_time)

        ranges = _generate_ranges(
            start_time=start_time,
            end_time=end_time,
            interval_minutes=interval_time,
        )

        time_range_objects = [
            TimeSlot(
                start_time=time_ranges["start_time"],
                end_time=time_ranges["end_time"],
                room_id=room_id,
            )
            for time_ranges in ranges
        ]

        db.add_all(time_range_objects)
        await db.commit()

        return {"message": "Time ranges saved successfully", "ranges": ranges}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@time_slot_router.get("/get_by_id/{time_slot_id}")
async def get_by_id(
    time_slot_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_by_id(model=TimeSlot, item_id=time_slot_id)


@time_slot_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    try:
        stmt = (
            select(TimeSlot)
            .join(Room, Room.id == TimeSlot.room_id)
            .join(UserLab, UserLab.lab_id == Room.lab_id)
            .where(UserLab.user_id == current_user.id)
        )
        result = await db.execute(stmt)
        time_slots_data = result.scalars().all()

        if not time_slots_data:
            raise HTTPException(status_code=404, detail="No time slots found")

        return time_slots_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@time_slot_router.delete("/delete/{time_slot_id}")
async def delete(
    time_slot_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    return await service.delete(model=TimeSlot, item_id=time_slot_id)
