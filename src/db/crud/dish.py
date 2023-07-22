import uuid
from typing import (
    Optional,
    Sequence,
)

from fastapi import Depends
from sqlalchemy import (
    Row,
    Select,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models
from src.db.core import get_db
from src.db.crud.abstract_crud import AbstractCRUD
from src.db.schemas.dish import (
    DishCreate,
    DishUpdate,
)


__all__ = (
    'DishCRUD',
    'get_dish_crud',
)


class DishCRUD(AbstractCRUD):
    """Database layer."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_statement(self) -> Select:
        """Get statement for execute from DB."""
        return select(
            self.dish_model.id,
            self.dish_model.title,
            self.dish_model.description,
            self.dish_model.submenu_id,
            self.dish_model.price,
        )

    async def _get_from_db(self, dish_id: uuid.UUID) -> Optional[models.Dish]:
        """Get dish for delete/update from DB."""
        stmt = select(
            self.dish_model
        ).where(self.dish_model.id == dish_id)

        result = await self.session.execute(
            statement=stmt
        )

        return result.scalar_one_or_none()

    async def get_detail(self, dish_id: uuid.UUID) -> Optional[models.Dish]:
        """Get detail of dish from DB."""
        stmt = self.get_statement().where(
            self.dish_model.id == dish_id)

        result = await self.session.execute(
            statement=stmt
        )

        return result.one_or_none()

    async def get_list(self, submenu_id: uuid.UUID) -> Sequence[Row]:
        """Get list of dishes from DB."""
        stmt = self.get_statement().where(
            self.dish_model.submenu_id == submenu_id)

        result = await self.session.execute(
            statement=stmt
        )

        return result.all()

    async def create(self,
                     submenu_id: uuid.UUID,
                     data: DishCreate) -> models.Dish:
        """Create new dish."""
        new_dish = self.dish_model(
            **data.model_dump(exclude_unset=True),
            submenu_id=submenu_id
        )

        self.session.add(new_dish)

        return new_dish

    async def update(self,
                     dish_id: uuid.UUID,
                     data: DishUpdate) -> Optional[models.Dish]:
        """Update exist dish."""
        dish = await self._get_from_db(dish_id)

        if dish:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(dish, key, value)
            self.session.add(dish)
            await self.session.commit()

        return dish

    async def delete(self, dish_id: uuid.UUID) -> bool:
        """Delete exist dish."""
        dish = await self._get_from_db(dish_id)

        if dish:
            await self.session.delete(dish)
            await self.session.commit()

            return True

        return False


async def get_dish_crud(
        session: AsyncSession = Depends(get_db)
) -> DishCRUD:
    """Instance of DishCRUD."""
    return DishCRUD(session=session)
