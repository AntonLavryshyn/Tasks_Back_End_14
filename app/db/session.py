from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# # The URL is now retrieved automatically and securely
DATABASE_URL = settings.DATABASE_URL_asyncpg

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False, # change on True if you need to see SQL-requests in terminal
    pool_pre_ping=True
)

# Factory of async sessions
AsyncSessionLocal = async_sessionmaker (
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for our ORM models (which you will create in app/db/ or separate models folder)
class Base(DeclarativeBase):
    pass

# Generator-function for getting session in routes
async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
