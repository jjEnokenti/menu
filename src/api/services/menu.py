import uuid
from functools import partial
from typing import Sequence

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import Row

from src.api import keys_for_cache_invalidation
from src.api.repositories.menu import MenuRepository
from src.api.schemas import MenuCreate, MenuUpdate, Status
from src.cache.service import CacheService
from src.db import models


class MenuService:
    """Menu service layer."""

    def __init__(self, repo: MenuRepository, cache: CacheService):
        self.repo = repo
        self.cache = cache

    async def get_detail(
            self,
            menu_id: uuid.UUID,
    ) -> Row | None:
        """Get detail of menu from cache or DB."""

        menu = await self.cache.get_obj_from_cache(
            keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
        )

        if menu:
            return menu

        try:
            menu = await self.repo.get_detail(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if menu:
            await self.cache.set_value_into_cache(
                keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
                menu
            )

            return menu

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )

    async def get_list(self) -> Sequence[Row]:
        """Get list of menus from cache or DB."""

        menus = await self.cache.get_obj_from_cache(
            keys_for_cache_invalidation.MENUS_LIST,
        )

        if menus:
            return menus

        try:
            menus = await self.repo.get_list()
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )
        if menus:
            await self.cache.set_value_into_cache(
                keys_for_cache_invalidation.MENUS_LIST,
                menus,
            )

        return menus

    async def get_all_detail_data(self) -> list:
        """Get all data from database."""
        items = await self.cache.get_obj_from_cache(keys_for_cache_invalidation.ALL_DATA)

        if not items:

            try:
                items = await self.repo.get_all_detail_data()
            except Exception as error:
                raise HTTPException(
                    detail=error.args, status_code=status.HTTP_400_BAD_REQUEST
                )

            if items:
                await self.cache.set_value_into_cache(
                    key=keys_for_cache_invalidation.ALL_DATA,
                    value=items
                )

        return [item.as_dict() for item in items]

    async def create(
            self,
            data: MenuCreate,
            background_tasks: BackgroundTasks,
    ) -> models.Menu:
        """Create new menu and invalidate cache."""

        try:
            async with self.repo.session.begin():
                new_menu = await self.repo.create(data.model_dump())

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        background_tasks.add_task(
            partial(
                self.cache.cache_invalidate,
                keys_for_cache_invalidation.MENUS_LIST,
            )
        )

        return new_menu

    async def update(
            self,
            menu_id: uuid.UUID,
            data: MenuUpdate,
            background_tasks: BackgroundTasks,
    ) -> models.Menu | None:
        """Update menu and invalidate cache."""

        try:
            async with self.repo.session.begin():
                menu = await self.repo.update(
                    menu_id=menu_id,
                    data=data.model_dump(exclude_unset=True),
                )

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

        background_tasks.add_task(
            partial(
                self.cache.cache_invalidate,
                keys_for_cache_invalidation.MENUS_LIST,
                keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
            )
        )

        return menu

    async def delete(
            self,
            menu_id: uuid.UUID,
            background_tasks: BackgroundTasks,
    ) -> Status:
        """Delete menu and invalidate cache."""

        try:
            async with self.repo.session.begin():
                is_deleted = await self.repo.delete(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if is_deleted:
            background_tasks.add_task(
                partial(
                    self.cache.cache_invalidate,
                    keys_for_cache_invalidation.MENUS_LIST,
                    keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
                    invalid_key=menu_id,
                )
            )

            return Status(status=f'Menu {menu_id} was successfully deleted!')

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )
