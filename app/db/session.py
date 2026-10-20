import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

#URL for async connection( in future pull the settings from the configuration file )
# First look for the variable in the Docker enviroument, if it's not there, use the local default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://my_user:my_password@localhost:5432/my_database")

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
