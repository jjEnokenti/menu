import uuid
from typing import Sequence

from sqlalchemy import Row, Select, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.repositories.abstract_repository import AbstractRepository
from src.db import models

__all__ = (
    'MenuRepository',
)


class MenuRepository(AbstractRepository):
    """Menu repository."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = models.Menu
        self.submenu_model = models.Submenu
        self.dish_model = models.Dish

    def get_statement(self) -> Select:
        """Get query for execute from DB."""

        return select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(distinct(self.submenu_model.id)).label('submenus_count'),
            func.count(self.submenu_model.dishes).label('dishes_count'),
        ).join(
            self.submenu_model,
            self.model.id == self.submenu_model.menu_id,
            isouter=True
        ).join(
            self.dish_model,
            self.submenu_model.id == self.dish_model.submenu_id,
            isouter=True
        ).group_by(
            self.model.id
        )

    async def get_all_detail_data(self) -> list[dict]:
        """Get all data."""

        items = await self.session.execute(
            select(
                self.model
            ).options(
                joinedload(models.Menu.submenus).joinedload(models.Submenu.dishes)
            )
        )

        return [item.as_dict() for item in items.scalars().unique().all()]

    async def get_detail(self, uid: uuid.UUID) -> Row | None:
        """Get detail of menu from DB."""

        result = await self.session.execute(
            statement=self.get_statement().where(self.model.id == uid)
        )

        return result.first()

    async def get_list(self) -> Sequence[Row]:
        """Get list method."""

        result = await self.session.execute(
            statement=self.get_statement()
        )

        return result.all()

    async def create(self, data: dict, **kwargs) -> models.Menu:
        """Create new menu."""

        menu = self.model(**data, **kwargs)

        self.session.add(menu)

        return menu

    async def update(
            self,
            menu_id: uuid.UUID,
            data: dict,
    ) -> models.Menu | None:
        """Update menu."""

        menu = await self._get_from_db(menu_id)

        for key, value in data.items():
            setattr(menu, key, value)
        self.session.add(menu)

        return menu

    async def delete(self, menu_id: uuid.UUID) -> bool:
        """Delete menu."""

        menu = await self._get_from_db(menu_id)

        if menu:
            await self.session.delete(menu)
            return True

        return False

    async def _get_from_db(self, menu_id: uuid.UUID) -> models.Menu | None:
        """Get menu from DB for delete/update."""

        result = await self.session.execute(
            select(
                self.model,
            ).options(
                joinedload(self.model.submenus).joinedload(self.submenu_model.dishes)
            ).where(self.model.id == menu_id)
        )

        return result.unique().scalar_one_or_none()
