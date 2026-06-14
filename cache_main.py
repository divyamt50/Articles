import os
import json
import asyncio
from redis import asyncio as aioredis

redis_url = "redis://localhost:6379/0"

redis_client = aioredis.from_url(redis_url, decode_response = True)

async def main():
    await redis_client.set("demo:greeting", "hello from python", ex=60)
    print("got:", await redis_client.get("demo:greeting"))
    print("ttl:", await redis_client.ttl("demo:greeting"))

    await redis_client.set("object:user1", json.dumps({"id":1, "name":"Alex"}), ex = 60)
    obj = json.loads(await redis_client.get("object:user1"))
    print(obj)

    await redis_client.delete("object:user1")
    print(await redis_client.get("object:user1"))

asyncio.run(main())