from contextlib import asynccontextmanager

# Importing framework and our connections
from fastapi import FastAPI
from db.session import async_engine
from core.redis import redis_client
from core.logger import logger

# importing ...
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logic during application startup
    logger.info("Launching a FastAPI application inside Docker")

    try:
        # Check Redis connection
        await redis_client.ping()
        logger.info("✅ Successfully connected to Redis.")
    except Exception as e:
        logger.error(f"❌ Error connecting to Redis: {str(e)}", exc_info=True)

    try:
        # Simple test of asynchronous database engine
        async with async_engine.connect() as conn:
            logger.info("✅ Successfully connected to PostgreSQL.")
    except Exception as e:
        logger.error(f"❌ Error connecting to PostgreSQL: {str(e)}", exc_info=True)

    yield

    # Logic during app shut down - simply close all connections
    logger.info("Stopping FastAPI application. Closing all connections ...")
    try:
        await redis_client.aclose()
        logger.info("Connection to Redis successfully closed.")
    except Exception as e:
        logger.error(f"Error while closing Redis: {str(e)} ")

    try:
        await async_engine.dispose()
        logger.info("The PostgreSQL connection pull has been successfully cleared ")
    except Exception as e:
        logger.error(f"Error while clearing up the PostgreSQL pool: {str(e)}")


# Passing lifespan to app
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {
        "status": 200,
        "detail": "ok",
        "result": "working"
    }

@app.get("/test")
async def test():
    return {"test": "working"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)