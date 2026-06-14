import os 
from dotenv import load_dotenv
load_dotenv()
from redis import asyncio as aioredis
from fastapi import HTTPException

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

r = aioredis.from_url(redis_url, decode_response = True)


TIER_LIMITS = {"free":5, "pro":100}
WINDOW_SECONDS = 60


async def rate_limiting(user_id:int, tier:int):
    key = f"user_request:{user_id}"
    curr_val = await r.incr(key)

    if curr_val == 1:
        await r.expire(key, WINDOW_SECONDS)

    user_tier_limit = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

    if not curr_val < user_tier_limit:
        ttl = await r.ttl(key)
        raise HTTPException(status_code=429, detail=f"Request count exceeded, try again in {ttl} seconds")