from abc import ABC, abstractmethod


class AbstractCache(ABC):

    @abstractmethod
    async def get(self, *args, **kwargs) -> list | dict | None:
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
