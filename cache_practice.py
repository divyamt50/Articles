import os
from dotenv import load_dotenv
load_dotenv()
from models import Article
from redis import asyncio as aioredis
import json
from schemas_demo import ArticleRead

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")


redis_client = aioredis.from_url(redis_url, decode_response = True)
r = redis_client

async def get_article(session, id:int):
    key = f"article:{id}"
    cached = await r.get(key)
    if cached:
        return ArticleRead.model_validate_json(cached)
    article = await session.get(Article, id)
    data = ArticleRead.model_validate(article)
    if article:
        await r.set(key, data.model_dump_json(), ex = 60)
        return article
    else:
        return None