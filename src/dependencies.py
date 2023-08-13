from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.dish import DishRepository
from src.api.repositories.menu import MenuRepository
from src.api.repositories.submenu import SubmenuRepository
from src.api.services.dish import DishService
from src.api.services.menu import MenuService
from src.api.services.submenu import SubmenuService
from src.cache.cache import RedisCache
from src.cache.core import get_redis_instance
from src.cache.service import CacheService
from src.db.core import get_db

__all__ = (
    'get_menu_repo',
    'get_submenu_repo',
    'get_dish_repo',
    'get_cache_repo',
    'get_cache_service',
    'get_menu_service',
    'get_submenu_service',
    'get_dish_service',
)


async def get_menu_repo(
        session: AsyncSession = Depends(get_db),
) -> MenuRepository:
    """Instance of MenuRepository."""
    return MenuRepository(session=session)


async def get_submenu_repo(
        session: AsyncSession = Depends(get_db),
) -> SubmenuRepository:
    """Instance of SubmenuRepository."""
    return SubmenuRepository(session=session)


async def get_dish_repo(
        session: AsyncSession = Depends(get_db),
) -> DishRepository:
    """Instance of DishRepository."""
    return DishRepository(session=session)


async def get_cache_repo(
        cache: Redis = Depends(get_redis_instance),
) -> RedisCache:
    """Get cache"""
    return RedisCache(cache=cache)


async def get_cache_service(
        cache: RedisCache = Depends(get_cache_repo),
) -> CacheService:
    """Instance of CacheService."""
    return CacheService(cache=cache)


async def get_menu_service(
        repo: MenuRepository = Depends(get_menu_repo),
        cache: CacheService = Depends(get_cache_service),
) -> MenuService:
    """Instance of MenuService."""

    return MenuService(repo=repo, cache=cache)


async def get_submenu_service(
        repo: SubmenuRepository = Depends(get_submenu_repo),
        cache: CacheService = Depends(get_cache_service),
) -> SubmenuService:
    """Instance of SubmenuService."""
    return SubmenuService(repo=repo, cache=cache)


async def get_dish_service(
        repo: DishRepository = Depends(get_dish_repo),
        cache: CacheService = Depends(get_cache_service),
) -> DishService:
    """Instance of DishService."""

    return DishService(repo=repo, cache=cache)
