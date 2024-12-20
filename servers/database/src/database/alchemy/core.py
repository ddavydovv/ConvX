from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from servers.database.src.config import settings


async_engine = create_async_engine(settings.alchemy.url, echo=True, future=True)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
Base = declarative_base()
