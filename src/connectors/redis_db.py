from redis.asyncio import Redis
from src.settings import settings

redis_host = settings.redis_host
redis_port = settings.redis_port
redis_user = settings.redis_user
redis_pass = settings.redis_pass

redis_db = Redis(
    host=redis_host,
    port=redis_port,
    username=redis_user,
    password=redis_pass,
    decode_responses=True,
)

