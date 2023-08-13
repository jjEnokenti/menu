from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    'AbstractRepository',
)


class AbstractRepository(ABC):
    """Abstract repository."""
    session: AsyncSession

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
