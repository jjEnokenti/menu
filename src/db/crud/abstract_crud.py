from abc import (
    ABC,
    abstractmethod,
)
from typing import Type

from src.db import models


class AbstractCRUD(ABC):
    """Abstract class for CRUD."""
    menu_model: Type[models.Menu] = models.Menu
    submenu_model: Type[models.Submenu] = models.Submenu
    dish_model: Type[models.Dish] = models.Dish

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
