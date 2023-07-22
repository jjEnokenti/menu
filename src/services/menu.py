import uuid
from typing import (
    Sequence,
    Union,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import Row

from src.db.crud.menu import (
    MenuCRUD,
    get_menu_crud,
)
from src.db.schemas.menu import (
    MenuCreate,
    MenuResponse,
    MenuUpdate,
    Status,
)
from src.services.abstract_service import AbstractService


class MenuService(AbstractService):
    """Service layer."""
    def __init__(self, crud: MenuCRUD):
        self.crud = crud

    async def get_detail(self, menu_id: uuid.UUID) -> Union[MenuResponse, Exception]:
        """Get detail of menu from DB layer."""
        try:
            menu = await self.crud.get_detail(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not menu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found'
                )

        return MenuResponse.model_validate(menu)

    async def get_list(self) -> Union[Sequence[Row], Exception]:
        """Get list of menus from DB layer."""
        try:
            menus = await self.crud.get_list()
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )

        return menus

    async def create(self, data: MenuCreate) -> Union[MenuResponse, Exception]:
        """Create new menu logic."""
        try:
            async with self.crud.session.begin():
                new_menu = await self.crud.create(data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )

        return MenuResponse.model_validate(new_menu)

    async def update(self, menu_id: uuid.UUID, data: MenuUpdate) -> Union[MenuResponse, Exception]:
        """Update menu logic."""
        try:
            async with self.crud.session.begin():
                menu = await self.crud.update(menu_id=menu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not menu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='menu not found'
                )

        return MenuResponse.model_validate(menu)

    async def delete(self, menu_id: uuid.UUID) -> Status:
        """Delete menu logic."""
        try:
            async with self.crud.session.begin():
                is_deleted = await self.crud.delete(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
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
