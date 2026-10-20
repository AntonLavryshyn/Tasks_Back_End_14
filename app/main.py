from contextlib import asynccontextmanager

# Importing framework and our connections
from fastapi import FastAPI
from db.session import async_engine
from core.redis import redis_client

# importing ...
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logic during start (if it needed)
    yield
    # Logic during stoping application - cleanly close all connections
    await redis_client.aclose()
    await async_engine.dispose()

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