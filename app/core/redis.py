import os
import redis.asyncio as aioredis

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis_cache://localhost:6379/0"
)

# Creating global Redis client
redis_client = aioredis.from_url(REDIS_URL, decode_responce=True)

# Generator for using in routes across Dependency Injections
async def get_redis_client():
    yield redis_client

