import json

from connectors.redis_db import redis_db
from settings import settings

CACHE_TTL = settings.redis_cache_ttl


async def save_cache(cache_key: str, cache_data: dict):
    """Сохранение записи в redis"""

    await redis_db.set(
        cache_key,
        json.dumps(cache_data, default=str),
        ex=CACHE_TTL,
    )


async def get_cache(cache_key):
    """Получение кэшированной записи из redis"""

    cached = await redis_db.get(cache_key)
    if cached:
        return json.loads(cached)


