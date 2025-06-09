import asyncio
from collections.abc import Callable
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base import get_db
from src.core.config import settings
from src.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user or not verify_password(password, user.password):
        return None
    return user


async def _create_token(data: dict, secret_key: str, expire_delta: timedelta) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expire_delta
    to_encode.update({"iat": now, "exp": expire})
    return await asyncio.to_thread(
        jwt.encode,
        to_encode,
        secret_key,
        algorithm=settings.ALGORITHM,
    )


async def create_access_token(data: dict) -> str:
    expire_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return await _create_token(data, settings.ACCESS_SECRET_KEY, expire_delta)


async def create_refresh_token(data: dict) -> str:
    expire_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return await _create_token(data, settings.REFRESH_SECRET_KEY, expire_delta)


async def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        role = payload.get("role")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token: 'sub' claim missing"
            )
        new_data = {"sub": username, "role": role}
        access_token = await create_access_token(new_data)
        return access_token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error{e}")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username not found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await get_user(db=db, username=username)
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def RoleChecker(valid_roles: str | list[str]) -> Callable:
    async def _role_checker(user: User = Depends(get_current_user)):
        roles = [valid_roles] if isinstance(valid_roles, str) else valid_roles
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail=f"Role '{user.role}' not allowed",
            )
        return user

    return _role_checker
