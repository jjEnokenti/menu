from abc import ABC, abstractmethod

from aioredis import Redis

from src.cache.core import get_redis_instance

__all__ = (
    'AbstractCache',
    'RedisCache',
    'get_redis',
)


class AbstractCache(ABC):

    @abstractmethod
    async def get(self, *args, **kwargs) -> bytes | None:
        """Abstract get data by key method require for implementation."""
        pass

    @abstractmethod
    async def set(self, *args, **kwargs) -> None:
        """Abstract set data method require for implementation."""
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        """Abstract remove data by keys method require for implementation."""
        pass

    @abstractmethod
    async def flush_all(self) -> None:
        """Abstract remove all data method require for implementation."""
        pass


class RedisCache(AbstractCache):
    """Redis repository,"""

    def __init__(self, cache: Redis):
        self.cache = cache

    async def get_keys_by_pattern(self, pattern: str = '*') -> list[bytes]:
        """Get keys from cache by pattern."""
        return await self.cache.keys(pattern)

    async def get(self, key: str) -> bytes | None:
        """Get data from cache by key."""
        return await self.cache.get(key)

    async def set(self, key: str, value: bytes, ex: int) -> None:
        """Set data into cache."""
        await self.cache.set(
            name=key,
            value=value,
            ex=ex,
        )

    async def delete(self, keys: list[str]) -> None:
        """Remove data from cache by keys."""

        await self.cache.unlink(*keys)

    async def flush_all(self) -> None:
        """Remove all data from cache."""

        await self.cache.flushall()


async def get_redis():
    return RedisCache(await get_redis_instance())
