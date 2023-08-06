from abc import ABC, abstractmethod

from src.cache.abstract_cache import AbstractCache
from src.repositories.abstract_repository import AbstractRepository


class AbstractService(ABC):
    """Abstract service class."""
    repo: AbstractRepository
    cache: AbstractCache

    detail_menu = 'menu:{}'
    menus_list = 'list_of_menus'

    detail_submenu = 'menu:{0}:submenu:{1}'
    submenus_list = 'menu:{}:list_of_submenus'

    detail_dish = 'menu:{0}:submenu:{1}:dish:{2}'
    dishes_list = 'menu:{0}:submenu:{1}:list_of_dishes'

    @abstractmethod
    async def get_detail(self, *args, **kwargs):
        """Abstract get detail method require for implementation."""
        pass

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        """Abstract get list method require for implementation."""
        pass

    @abstractmethod
    async def create(self, *args, **kwargs):
        """Abstract create method require for implementation."""
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        """Abstract update method require for implementation."""
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        """Abstract delete method require for implementation."""
        pass

    async def get_obj_from_cache(self, key: str):
        """Get object from cache method."""
        try:
            obj = await self.cache.get(self.detail_menu.format(key))
        except Exception:
            obj = None

        return obj

    async def set_value_into_cache(self, key, value):
        """Set object into cache method."""
        try:
            await self.cache.set(key, value)
        except Exception:
            pass

    async def cache_invalidate(self, *args, **kwargs):
        """Delete objects from cache method."""
        try:
            await self.cache.delete(args, **kwargs)
        except Exception:
            pass
