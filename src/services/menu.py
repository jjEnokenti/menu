import uuid
from typing import (
    Optional,
    Sequence,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import Row

from src.db import models
from src.db.crud.menu import (
    MenuCRUD,
    get_menu_crud,
)
from src.db.schemas import Status
from src.db.schemas.menu import (
    MenuCreate,
    MenuUpdate,
)
from src.services.abstract_service import AbstractService


class MenuService(AbstractService):
    """Service layer."""

    def __init__(self, crud: MenuCRUD):
        self.crud = crud

    async def get_detail(self, menu_id: uuid.UUID) -> Optional[models.Menu]:
        """Get detail of menu from DB layer."""
        try:
            menu = await self.crud.get_detail(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0].split(':')[2].strip()
            )
        else:
            if not menu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found'
                )

        return menu

    async def get_list(self) -> Sequence[Row]:
        """Get list of menus from DB layer."""
        try:
            menus = await self.crud.get_list()
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0].split(':')[2].strip()
            )

        return menus

    async def create(self, data: MenuCreate) -> Optional[models.Menu]:
        """Create new menu logic."""
        try:
            async with self.crud.session.begin():
                new_menu = await self.crud.create(data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0].split(':')[2].strip()
            )

        return new_menu

    async def update(self,
                     menu_id: uuid.UUID,
                     data: MenuUpdate) -> Optional[models.Menu]:
        """Update menu logic."""
        try:
            async with self.crud.session.begin():
                menu = await self.crud.update(menu_id=menu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0].split(':')[2].strip()
            )
        else:
            if not menu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found'
                )

        return menu

    async def delete(self, menu_id: uuid.UUID) -> Status:
        """Delete menu logic."""
        try:
            async with self.crud.session.begin():
                is_deleted = await self.crud.delete(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0].split(':')[2].strip()
            )
        else:
            if not is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found'
                )

        return Status(message=f'Menu {menu_id} was successfully deleted!')


async def get_menu_service(
        crud: MenuCRUD = Depends(get_menu_crud)
) -> MenuService:
    """Instance of MenuService."""
    return MenuService(crud=crud)
