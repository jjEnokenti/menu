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
from src.db.crud.submenu import (
    SubmenuCRUD,
    get_submenu_crud,
)
from src.db.schemas import Status
from src.db.schemas.submenu import (
    SubmenuCreate,
    SubmenuUpdate,
)
from src.services.abstract_service import AbstractService


class SubmenuService(AbstractService):
    """Service layer."""

    def __init__(self, crud: SubmenuCRUD):
        self.crud = crud

    async def get_detail(self,
                         submenu_id: uuid.UUID) -> Optional[models.Submenu]:
        """Get detail of submenu from DB layer."""
        try:
            submenu = await self.crud.get_detail(submenu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not submenu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='submenu not found'
                )

        return submenu

    async def get_list(self, menu_id: uuid.UUID) -> Sequence[Row]:
        """Get list of submenus from DB layer."""
        try:
            submenus = await self.crud.get_list(menu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )

        return submenus

    async def create(self,
                     menu_id: uuid.UUID,
                     data: SubmenuCreate) -> Optional[models.Submenu]:
        """Create new submenu logic."""
        try:
            async with self.crud.session.begin():
                new_submenu = await self.crud.create(menu_id=menu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )

        return new_submenu

    async def update(self,
                     submenu_id: uuid.UUID,
                     data: SubmenuUpdate) -> Optional[models.Submenu]:
        """Update submenu logic."""
        try:
            async with self.crud.session.begin():
                submenu = await self.crud.update(submenu_id=submenu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not submenu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='submenu not found'
                )

        return submenu

    async def delete(self, submenu_id: uuid.UUID) -> Status:
        """Delete submenu logic."""
        try:
            async with self.crud.session.begin():
                is_deleted = await self.crud.delete(submenu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='submenu not found'
                )

        return Status(message=f'Submenu {submenu_id} was successfully deleted!')


async def get_submenu_service(
        crud: SubmenuCRUD = Depends(get_submenu_crud)
) -> SubmenuService:
    """Instance of SubmenuService."""
    return SubmenuService(crud=crud)
