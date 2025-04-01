from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_timeout=30,  # Timeout for getting a connection from the pool (in seconds)
    pool_recycle=1800, # Recycle connections every 30 minutes (in seconds)
)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def add_postgresql_extension() -> None:
    async with SessionLocal() as db:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        await db.execute(query)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

