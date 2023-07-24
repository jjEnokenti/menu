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
from src.db.crud.dish import (
    DishCRUD,
    get_dish_crud,
)
from src.db.schemas import Status
from src.db.schemas import dish as dish_schemas
from src.db.schemas.dish import DishResponse
from src.services.abstract_service import AbstractService


class DishService(AbstractService):
    """Service layer."""

    def __init__(self, crud: DishCRUD):
        self.crud = crud

    async def get_detail(self,
                         dish_id: uuid.UUID) -> Optional[models.Dish]:
        """Get detail of dish from DB layer."""
        try:
            dish = await self.crud.get_detail(dish_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not dish:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='dish not found'
                )

        return dish

    async def get_list(self, submenu_id: uuid.UUID) -> Sequence[Row]:
        """Get list of dishes from DB layer."""
        try:
            dishes = await self.crud.get_list(submenu_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        if not dishes:
            return []

        return dishes

    async def create(self,
                     submenu_id: uuid.UUID,
                     data: dish_schemas.DishCreate) -> Optional[models.Dish]:
        """Create new dish logic."""
        try:
            async with self.crud.session.begin():
                new_dish = await self.crud.create(submenu_id=submenu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )

        return new_dish

    async def update(self,
                     dish_id: uuid.UUID,
                     data: dish_schemas.DishUpdate) -> Optional[models.Dish]:
        """Update dish logic."""
        try:
            async with self.crud.session.begin():
                dish = await self.crud.update(dish_id=dish_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not dish:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='dish not found'
                )

        return dish

    async def delete(self, dish_id: uuid.UUID) -> Status:
        """Delete dish logic."""
        try:
            async with self.crud.session.begin():
                is_deleted = await self.crud.delete(dish_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args[0]
            )
        else:
            if not is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='dish not found'
                )

        return Status(message=f'Dish {dish_id} was successfully deleted!')


async def get_dish_service(
        crud: DishCRUD = Depends(get_dish_crud)
) -> DishService:
    """Instance of DishService."""
    return DishService(crud=crud)
