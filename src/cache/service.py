import pickle
import uuid
from typing import Sequence

from aioredis import exceptions
from sqlalchemy import Row

from src.api.keys_for_cache_invalidation import ALL_DATA
from src.cache.cache import RedisCache, get_redis


class CacheService:

    def __init__(self, cache: RedisCache):
        self.cache = cache

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
            value: Sequence | Row,
    ) -> None:
        """Set data into cache method."""
        try:
            value = pickle.dumps(value)
            await self.cache.set(key, value)
        except exceptions.RedisError as error:
            # todo: add logging
            print(error.args)

    async def cache_invalidate(
            self, *args,
            invalid_key: uuid.UUID | None = None,
    ) -> None:
        """Delete data from cache method by keys."""
        keys = list(args) + [ALL_DATA]

        try:
            if invalid_key:
                cache_keys = await self.cache.get_keys_by_pattern(
                    pattern=rf'*{str(invalid_key)}*'
                )
                keys.extend(cache_keys)

            await self.cache.delete(keys)
        except exceptions.RedisError as error:
            # todo: add logging
            print(error.args)


async def get_cache():
    return CacheService(await get_redis())
