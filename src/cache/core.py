from aioredis import Redis

from src.config import settings


async def get_redis_cache() -> Redis:
    """Redis cache configurate instance."""
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
