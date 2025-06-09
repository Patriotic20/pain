import asyncio
import pytest
from sqlalchemy.ext.asyncio import ( 
    create_async_engine, 
    AsyncSession, 
    async_sessionmaker
    )

from src.core.base import Base
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str
    DB_HOST: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_NAME: str


    @property
    def connection_string(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".test.env")

settings = Settings()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def engine():
    engine = create_async_engine(settings.connection_string , echo = False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




async def db_session(engine: AsyncEngine = Depends(engine)):
    async_session = async_sessionmaker(
        engine, expire_on_commit=False , class_=AsyncSession
    )

    async with async_session() as session:
        yield session