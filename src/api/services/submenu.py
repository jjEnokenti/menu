import uuid
from functools import partial
from typing import Sequence

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import Row

from src.api import keys_for_cache_invalidation
from src.api.repositories.submenu import SubmenuRepository
from src.api.schemas import Status, SubmenuCreate, SubmenuUpdate
from src.cache.service import CacheService
from src.db import models


class SubmenuService:
    """Submenu service layer."""

    def __init__(self, repo: SubmenuRepository, cache: CacheService):
        self.repo = repo
        self.cache = cache

    async def get_detail(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
    ) -> Row | None:
        """Get detail of submenu from cache or DB."""

        submenu = await self.cache.get_obj_from_cache(
            keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, submenu_id)
        )

        if submenu:
            return submenu

        try:
            submenu = await self.repo.get_detail(
                submenu_id=submenu_id,
                menu_id=menu_id,
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if submenu:
            await self.cache.set_value_into_cache(
                keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, submenu_id),
                submenu,
            )

            return submenu

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )

    async def get_list(
            self,
            menu_id: uuid.UUID,
    ) -> Sequence[Row]:
        """Get list of submenus from cache or DB."""

        submenus = await self.cache.get_obj_from_cache(
            keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id)
        )

        if submenus:
            return submenus

        try:
            submenus = await self.repo.get_list(menu_id=menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if submenus:
            await self.cache.set_value_into_cache(
                keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id),
                submenus,
            )

        return submenus

    async def create(
            self,
            menu_id: uuid.UUID,
            data: SubmenuCreate,
            background_tasks: BackgroundTasks,
    ) -> models.Submenu:
        """Create new submenu and invalidate cache."""

        try:
            async with self.repo.session.begin():
                new_submenu = await self.repo.create(
                    data=data.model_dump(),
                    menu_id=menu_id,
                )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        background_tasks.add_task(
            partial(
                self.cache.cache_invalidate,
                keys_for_cache_invalidation.MENUS_LIST,
                keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
            )
        )

        return new_submenu

    async def update(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: SubmenuUpdate,
            background_tasks: BackgroundTasks,
    ) -> models.Submenu | None:
        """Update submenu and invalidate cache."""

        try:
            async with self.repo.session.begin():
                submenu = await self.repo.update(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    data=data.model_dump(exclude_unset=True),
                )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if submenu:
            background_tasks.add_task(
                partial(
                    self.cache.cache_invalidate,
                    keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, submenu_id),
                    keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id),
                )
            )

            return submenu

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )

    async def delete(
            self,
            submenu_id: uuid.UUID,
            menu_id: uuid.UUID,
            background_tasks: BackgroundTasks,
    ) -> Status:
        """Delete submenu and invalidate cache."""

        try:
            async with self.repo.session.begin():
                deleted_submenu = await self.repo.delete(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if deleted_submenu:
            background_tasks.add_task(
                partial(
                    self.cache.cache_invalidate,
                    keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, submenu_id),
                    keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id),
                    keys_for_cache_invalidation.MENUS_LIST,
                    keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
                    invalid_key=submenu_id,
                )
            )

            return Status(status=f'Submenu {submenu_id} was successfully deleted!')

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )
