from fastapi import APIRouter , Depends , HTTPException , status
from src.schemas.user import UserCreate , UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from src.models.user import User
from src.utils.auth import *

auth_router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)


@auth_router.post("/register" , response_model=UserResponse)
async def register(
    user_item: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        new_user = User(**user_item.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error {e}"
        )

@auth_router.post("/login")
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
    ):

    user = await authenticate_user(db , form_data.username , form_data.password)

    access_token = await create_access_token(
        {
            "sub" : user.username,
            "role" : user.role
        }
    )

    refresh_token = await create_refresh_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }



@auth_router.post("/refresh")
async def refresh(
    token: str
):
    tokens = await refresh_access_token(refresh_token=token)

    return {
        'access_token': tokens, 
        }
    

