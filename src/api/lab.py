from fastapi import APIRouter

from src.core.base import get_db
from src.models import Lab, User, UserLab
from src.schemas.lab import LabBase, LabUpdate, UserLabCreate , LabResponse
from src.utils import *
from src.utils.auth import *

lab_router = APIRouter(tags=["Lab"], prefix="/lab")


@lab_router.post("/create" , response_model=LabResponse)
async def create(
    lab_item: LabBase,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    exsit_lab_name = await service.get_by_field(model= Lab, field_name="name" , field_value=lab_item.name)
    if exsit_lab_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This name already used"
        )
    
    new_lab = Lab(**lab_item.model_dump())
    db.add(new_lab)
    await db.flush()

    new_relation = UserLabCreate(user_id=current_user.id, lab_id=new_lab.id)
    user_lab_data = await service.create(model=UserLab, db_obj=new_relation)

    return {
        "id": user_lab_data.lab_id,
        "name" : lab_item.name,
        "description" : lab_item.description
    }


@lab_router.get("/get_by_id/{lab_id}")
async def get_by_id(
    lab_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(UserLab, User, Lab)
        .join(User, User.id == UserLab.user_id)
        .join(Lab, Lab.id == UserLab.lab_id)
        .where(Lab.id == lab_id, User.id == current_user.id)
    )

    result = await db.execute(query)
    rows = result.all()

    output = [
        {
            "user_id": user.id,
            "username": user.username,
            "user_labs": {"lab_id": lab.id, "lab_name": lab.name},
        }
        for user_lab, user, lab in rows
    ]
    return output


@lab_router.get("/get_all")
async def get_all(
    current_user: User = Depends(RoleChecker("admin")),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(UserLab, User, Lab)
        .join(User, User.id == UserLab.user_id)
        .join(Lab, Lab.id == UserLab.lab_id)
    )
    result = await db.execute(query)
    rows = result.all()

    user_dict = {}
    for user_lab, user, lab in rows:
        if user.id not in user_dict:
            user_dict[user.id] = {
                "user_id": user.id,
                "username": user.username,
                "user_labs": []
            }
        user_dict[user.id]["user_labs"].append({
            "lab_id": lab.id,
            "lab_name": lab.name
        })

    # Convert to list format
    output = list(user_dict.values())
    return output


@lab_router.put("/update/{lab_id}")
async def update(
    lab_id: int,
    lab_item: LabUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    query = select(UserLab).where(
        UserLab.lab_id == lab_id, UserLab.user_id == current_user.id
    )

    result = await db.execute(query)
    user_lab = result.scalars().first()
    if not user_lab:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this lab.",
        )

    return await service.update(model=Lab, item_id=lab_id, db_obj=lab_item)


@lab_router.delete("/delete/{lab_id}")
async def delete(
    lab_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    query = select(UserLab).where(
        UserLab.lab_id == lab_id, UserLab.user_id == current_user.id
    )
    result = await db.execute(query)
    user_lab = result.scalars().first()

    if not user_lab:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this lab.",
        )

    await service.delete(model=UserLab, item_id=user_lab.id)
    await service.delete(model=Lab, item_id=lab_id)

    return {"detail": "Lab deleted successfully."}
