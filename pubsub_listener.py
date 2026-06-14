import asyncio
from redis import asyncio as aioredis
import os



async def listen_events():

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    r = aioredis.from_url(redis_url, decode_responses = True)
    pubsub = r.pubsub()
    await pubsub.subscribe("new_artiles")

    async for message in pubsub.listen():
        if message["type"] == "message":
            print(f"message {message["data"]}")


if __name__ == "__main__":
    asyncio.run(listen_events())