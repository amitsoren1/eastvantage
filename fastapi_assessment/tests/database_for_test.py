from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import TEST_DB_URL
from database import get_db
from models import Base
from main import get_db, app


engine = create_async_engine(TEST_DB_URL, pool_pre_ping=True, echo=False)

async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
