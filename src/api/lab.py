from fastapi import APIRouter
from src.schemas.lab import LabBase, LabUpdate, UserLabCreate
from src.utils.auth import *
from src.utils import *
from src.models import Lab, User, UserLab
from src.core.base import get_db

lab_router = APIRouter(tags=["Lab"], prefix="/lab")


@lab_router.post("/create")
async def create(
    lab_item: LabBase,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db),
):
    new_lab = Lab(**lab_item.model_dump())
    db.add(new_lab)
    await db.flush()

    new_relation = UserLabCreate(user_id=current_user.id, lab_id=new_lab.id)
    return await service.create(model=UserLab, db_obj=new_relation)


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

    output = [
        {
            "user_id": user.id,
            "username": user.username,
            "user_labs": {"lab_id": lab.id, "lab_name": lab.name},
        }
        for user_lab, user, lab in rows
    ]
    return output


@lab_router.put("/update/{lab_id}")
async def update(
    lab_id: int,
    lab_item: LabUpdate,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(UserLab)
        .where(UserLab.lab_id == lab_id , UserLab.user_id == current_user.id)
    )

    result = await db.execute(query)
    user_lab = result.scalars().first()
    if not user_lab:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this lab."
        )
    
    return await service.update(model=Lab, item_id=lab_id, db_obj=lab_item)


@lab_router.delete("/delete/{lab_id}")
async def delete(
    lab_id: int,
    current_user: User = Depends(RoleChecker("admin")),
    service: BaseService = Depends(get_base_service),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(UserLab)
        .where(UserLab.lab_id == lab_id, UserLab.user_id == current_user.id)
    )
    result = await db.execute(query)
    user_lab = result.scalars().first()

    if not user_lab:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this lab."
        )
    
    await service.delete(model=UserLab , item_id=user_lab.id)
    await service.delete(model=Lab, item_id=lab_id)

    return {"detail": "Lab deleted successfully."}
