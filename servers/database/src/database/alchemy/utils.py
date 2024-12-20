from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from servers.database.src.database.alchemy.core import Base, async_session, async_engine


async def create_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session as session:
        yield session