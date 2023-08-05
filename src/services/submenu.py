import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import Row

from src.cache.cache import Cache, get_cache
from src.db import models
from src.db.schemas import Status
from src.db.schemas.submenu import SubmenuCreate, SubmenuUpdate
from src.repositories.submenu import SubmenuRepository, get_submenu_repo
from src.services.abstract_service import AbstractService


class SubmenuService(AbstractService):
    """Service layer."""

    def __init__(self, repo: SubmenuRepository, cache: Cache):
        self.repo = repo
        self.cache = cache

    async def get_detail(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> Row | dict:
        """Get detail of submenu from cache or DB layer."""
        submenu = await self.get_obj_from_cache(
            self.detail_submenu.format(menu_id, submenu_id)
        )

        if not submenu:
            try:
                submenu = await self.repo.get_detail(submenu_id)
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )

        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )

        await self.set_value_into_cache(
            self.detail_submenu.format(menu_id, submenu_id),
            submenu
        )

        return submenu

    async def get_list(
            self,
            menu_id: uuid.UUID
    ) -> list | dict | None:
        """Get list of submenus from cache or DB layer."""
        submenus = await self.get_obj_from_cache(self.submenus_list.format(menu_id))

        if not submenus:
            try:
                submenus = await self.repo.get_list(menu_id)
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )

            if submenus:
                await self.set_value_into_cache(
                    self.submenus_list.format(menu_id),
                    submenus
                )

        return submenus

    async def create(
            self,
            menu_id: uuid.UUID,
            data: SubmenuCreate
    ) -> models.Submenu | None:
        """Create new submenu logic and remove from cache."""
        try:
            async with self.repo.session.begin():
                new_submenu = await self.repo.create(menu_id=menu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        await self.cache_invalidate(
            self.menus_list,
            self.detail_menu.format(menu_id)
        )

        return new_submenu

    async def update(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: SubmenuUpdate
    ) -> models.Submenu | None:
        """Update submenu logic and remove from cache."""
        try:
            async with self.repo.session.begin():
                submenu = await self.repo.update(submenu_id=submenu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        await self.cache_invalidate(
            self.detail_submenu.format(menu_id, submenu_id),
            self.submenus_list.format(menu_id)
        )

        return submenu

    async def delete(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> Status:
        """Delete submenu logic and remove from cache."""
        try:
            async with self.repo.session.begin():
                deleted_submenu = await self.repo.delete(submenu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if not deleted_submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        await self.cache_invalidate(
            self.detail_submenu.format(menu_id, submenu_id),
            self.submenus_list.format(menu_id),
            self.menus_list,
            self.detail_menu.format(menu_id),
            invalid_key=submenu_id
        )

        return Status(message=f'Submenu {submenu_id} was successfully deleted!')


async def get_submenu_service(
        repo: SubmenuRepository = Depends(get_submenu_repo),
        cache: Cache = Depends(get_cache)
) -> SubmenuService:
    """Instance of SubmenuService."""
    return SubmenuService(repo=repo, cache=cache)
