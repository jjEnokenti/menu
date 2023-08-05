import uuid

from fastapi import Depends, HTTPException, status

from src.cache.cache import Cache, get_cache
from src.db import models
from src.db.schemas import Status
from src.db.schemas.menu import MenuCreate, MenuUpdate
from src.repositories.menu import MenuRepository, get_menu_repo
from src.services.abstract_service import AbstractService


class MenuService(AbstractService):
    """Service layer."""

    def __init__(self, repo: MenuRepository, cache: Cache):
        self.repo = repo
        self.cache = cache

    async def get_detail(
            self,
            menu_id: uuid.UUID
    ) -> dict:
        """Get detail of menu from cache or DB layer."""
        menu = await self.get_obj_from_cache(self.detail_menu.format(menu_id))

        if not menu:
            try:
                menu = await self.repo.get_detail(menu_id)
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found'
            )

        await self.set_value_into_cache(
            self.detail_menu.format(menu_id),
            menu
        )

        return menu

    async def get_list(self) -> list:
        """Get list of menus from cache or DB layer."""
        menus = await self.get_obj_from_cache(self.menus_list)

        if not menus:
            try:
                menus = await self.repo.get_list()
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )
            if menus:
                await self.set_value_into_cache(
                    self.menus_list,
                    menus
                )

        return menus

    async def create(self, data: MenuCreate) -> models.Menu | None:
        """Create new menu logic and remove menus from cache."""
        try:
            async with self.repo.session.begin():
                new_menu = await self.repo.create(data)

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        await self.cache_invalidate(self.menus_list)

        return new_menu

    async def update(
            self,
            menu_id: uuid.UUID,
            data: MenuUpdate
    ) -> models.Menu | None:
        """Update menu logic and remove this menu and menus from cache."""
        try:
            async with self.repo.session.begin():
                menu = await self.repo.update(menu_id=menu_id, data=data)

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found'
            )
        await self.cache_invalidate(
            self.menus_list,
            self.detail_menu.format(menu_id),
        )

        return menu

    async def delete(self, menu_id: uuid.UUID) -> Status:
        """Delete menu logic and remove this menu and menus form cache."""
        try:
            async with self.repo.session.begin():
                is_deleted = await self.repo.delete(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if not is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found'
            )

        await self.cache_invalidate(
            self.menus_list,
            self.detail_menu.format(menu_id),
            invalid_key=menu_id
        )

        return Status(message=f'Menu {menu_id} was successfully deleted!')


async def get_menu_service(
        repo: MenuRepository = Depends(get_menu_repo),
        cache: Cache = Depends(get_cache)
) -> MenuService:
    """Instance of MenuService."""
    return MenuService(repo=repo, cache=cache)
