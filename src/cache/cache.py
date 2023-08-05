import pickle
from typing import Sequence

from aioredis import Redis
from fastapi import Depends
from sqlalchemy import Row

from src.cache.abstract_cache import AbstractCache
from src.cache.core import get_redis_cache
from src.config import settings


class Cache(AbstractCache):

    def __init__(self, cache: Redis):
        self.cache = cache

    async def get(self, key: str) -> list | dict | None:
        """Get data from cache by key."""
        value = await self.cache.get(key)

        return pickle.loads(value) if value else None

    async def set(self, key: str, value: Sequence[Row] | Row, ex: int = 30) -> None:
        """Set data into cache."""
        await self.cache.set(
            name=key,
            value=pickle.dumps(value),
            ex=settings.REDIS_CACHE_EXPIRE or ex,
        )

    async def delete(self, keys: list[str], invalid_key: str | None = None) -> None:
        """Remove data from cache by keys."""

        keys = list(map(str, keys))

        if invalid_key:
            cache_keys = await self.cache.keys(pattern=rf'*{str(invalid_key)}*')
            keys.extend(cache_keys)

        await self.cache.delete(*keys)

    async def flush_all(self) -> None:
        """Remove all data from cache."""

        await self.cache.flushall()


async def get_cache(
        cache: Redis = Depends(get_redis_cache)
) -> Cache:
    """Get cache"""
    return Cache(cache=cache)
