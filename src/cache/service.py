import decimal
import pickle
import uuid
from pathlib import Path
from typing import Sequence

from aioredis import exceptions
from loguru import logger
from sqlalchemy import Row

from src.api.keys_for_cache_invalidation import ALL_DATA
from src.cache.cache import RedisCache, get_redis
from src.config import settings

log_path = Path(f'{settings.BASE_DIR}/logs/cache')
log_path.mkdir(parents=True, exist_ok=True)

logger.add(f'{log_path}/cache_error.log', level='ERROR',
           format='{time} | [{level}] | {name}::{function}: line {line} | {message}', rotation='20 KB',
           compression='zip')


class CacheService:

    def __init__(self, cache: RedisCache):
        self.cache = cache

    async def get_keys_by_pattern(self, key: str) -> list:
        """Get keys from cache by pattern."""

        return [key.decode('utf-8') for key in await self.cache.get_keys_by_pattern(rf'*{key}*')]

    async def get_discount(self, key: str | uuid.UUID) -> str | None:
        """Get discount by key."""

        key = f'discount:{key}'

        discounts = await self.get_discounts()

        return discounts.get(key)

    async def get_discounts(self) -> dict:
        """Get all discount objects."""
        discounts = {}
        pattern = r'*discount*'

        keys = await self.get_keys_by_pattern(pattern)

        for key in keys:
            value = await self.get_obj_from_cache(key)
            discounts[key] = value

        return discounts

    async def get_obj_from_cache(self, key: str) -> Sequence | Row | None:
        """Get object from cache method."""
        try:
            value = await self.cache.get(key)
        except exceptions.RedisError:
            value = None

        return pickle.loads(value) if value else value

    async def set_value_into_cache(
            self,
            key: str,
            value: Sequence | Row | decimal.Decimal,
            ex: int | None = None,
    ) -> None:
        """Set data into cache method."""
        if ex is None:
            ex = settings.REDIS_CACHE_EXPIRE
        try:
            value = pickle.dumps(value)
            await self.cache.set(key, value, ex=ex)
        except exceptions.RedisError as error:
            logger.error(error)

    async def cache_invalidate(
            self, *args,
            invalid_key: uuid.UUID | None = None,
    ) -> None:
        """Delete data from cache method by keys."""
        keys = list(args) + [ALL_DATA]

        try:
            if invalid_key:
                cache_keys = await self.get_keys_by_pattern(rf'*{str(invalid_key)}*')
                keys.extend(cache_keys)

            await self.cache.delete(keys)
        except exceptions.RedisError as error:
            logger.error(error)


async def get_cache():
    return CacheService(await get_redis())
