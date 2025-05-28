from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine

from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///taller_database.db"

async_engine = create_async_engine(DATABASE_URL, echo=True)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session
