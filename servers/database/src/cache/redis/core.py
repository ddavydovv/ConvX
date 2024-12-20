import redis.asyncio as redis

from servers.database.src.config import settings


redis_client = redis.from_url(settings.cache.url)