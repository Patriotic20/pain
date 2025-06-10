from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse , UserBase
from src.utils.auth import *
from src.utils import BaseService , get_base_service

auth_router = APIRouter(tags=["Auth Admin"], prefix="/auth")


@auth_router.post("/register", response_model=UserResponse)
async def register(
    user_item: UserBase, 
    service : BaseService = Depends(get_base_service)
    ):

    user_data_existing = await service.get_by_field(model=User , field_name="username" , field_value=user_item.username)
    if user_data_existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already used"
        ) 
    user_password = hash_password(password=user_item.password)
    user_data = UserCreate(
        username=user_item.username,
        password=user_password,
        role= "admin"
    )

    return await service.create(model=User , db_obj=user_data)


@auth_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username , form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    access_token = await create_access_token({"sub": user.username, "role": user.role})

    refresh_token = await create_refresh_token(
        {"sub": user.username, "role": user.role}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/refresh")
async def refresh(token: str):
    tokens = await refresh_access_token(refresh_token=token)

    return {
        "access_token": tokens,
    }
