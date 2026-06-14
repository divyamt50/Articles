import json
import os
from redis import asyncio as aioredis

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = aioredis.from_url(redis_url, decode_response = True)


async def cache_get(key:str)->str|None:
    return await redis_client.get(key)

async def cache_set(key:str, value:str, ttl:int = 60)->None:
    await redis_client.set(key, value, ex=ttl)

async def cache_delete(key:str)->None:
    await redis_client.delete(key)