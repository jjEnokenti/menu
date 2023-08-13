import uuid
from typing import Sequence

from sqlalchemy import Row, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.abstract_repository import AbstractRepository
from src.db import models

__all__ = (
    'DishRepository',
)


class DishRepository(AbstractRepository):
    """Dish repository."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = models.Dish

    def get_statement(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
    ) -> Select:
        """Get statement for execute from DB."""

        return select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.submenu_id,
            self.model.price,
        ).where(
            self.model.submenu.has(menu_id=menu_id),
            self.model.submenu_id == submenu_id,
        )

    async def get_detail(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
    ) -> Row | None:
        """Get detail of dish from DB."""

        result = await self.session.execute(
            statement=self.get_statement(
                menu_id=menu_id,
                submenu_id=submenu_id,
            ).where(
                self.model.id == dish_id
            )
        )

        return result.first()

    async def get_list(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
    ) -> Sequence[Row]:
        """Get list of dishes from DB."""

        result = await self.session.execute(
            statement=self.get_statement(
                menu_id=menu_id,
                submenu_id=submenu_id,
            )
        )

        return result.all()

    async def create(self, data: dict, **kwargs) -> models.Dish:
        """Create new dish."""

        new_dish = self.model(**data, **kwargs)

        self.session.add(new_dish)

        return new_dish

    async def update(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            data: dict,
    ) -> models.Dish | None:
        """Update dish."""

        dish = await self._get_from_db(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )

        if dish:
            for key, value in data.items():
                setattr(dish, key, value)
            self.session.add(dish)
            await self.session.commit()

        return dish

    async def delete(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
    ) -> bool:
        """Delete dish."""

        dish = await self._get_from_db(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )

        if dish:
            await self.session.delete(dish)
            return True

        return False

    async def _get_from_db(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
    ) -> models.Dish | None:
        """Get dish for delete/update from DB."""

        result = await self.session.execute(
            select(self.model).where(
                self.model.submenu.has(menu_id=menu_id),
                self.model.submenu_id == submenu_id,
                self.model.id == dish_id,
            )
        )

        return result.scalar_one_or_none()
