import uuid
from typing import Sequence

from fastapi import Depends
from sqlalchemy import Row, Select, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models
from src.db.core import get_db
from src.db.schemas.menu import MenuCreate, MenuUpdate
from src.repositories.abstract_repository import AbstractRepository

__all__ = (
    'MenuRepository',
    'get_menu_repo',
)


class MenuRepository(AbstractRepository):
    """Database layer."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_statement(self) -> Select:
        """Get query for execute from DB."""

        return select(
            self.menu_model.id,
            self.menu_model.title,
            self.menu_model.description,
            func.count(distinct(self.submenu_model.id)).label('submenus_count'),
            func.count(self.submenu_model.dishes).label('dishes_count')
        ).join(
            self.submenu_model,
            self.menu_model.id == self.submenu_model.menu_id,
            isouter=True
        ).join(
            self.dish_model,
            self.submenu_model.id == self.dish_model.submenu_id,
            isouter=True
        ).group_by(
            self.menu_model.id
        )

    async def _get_from_db(self, menu_id: uuid.UUID) -> models.Menu | None:
        """Get menu for delete/update from DB."""
        stmt = select(
            self.menu_model
        ).where(self.menu_model.id == menu_id)

        result = await self.session.execute(
            statement=stmt
        )

        return result.scalar_one_or_none()

    async def get_detail(self, menu_id: uuid.UUID) -> models.Menu | None:
        """Get detail of menu from DB."""
        stmt = self.get_statement().where(self.menu_model.id == menu_id)

        result = await self.session.execute(
            statement=stmt
        )

        return result.first()

    async def get_list(self) -> Sequence[Row]:
        """Get list of menu from DB."""
        stmt = self.get_statement()

        result = await self.session.execute(
            statement=stmt,
        )

        return result.all()

    async def create(self, data: MenuCreate) -> models.Menu:
        """Create new menu."""
        new_menu = self.menu_model(**data.model_dump(exclude_unset=True))

        self.session.add(new_menu)

        return new_menu

    async def update(
            self,
            menu_id: uuid.UUID,
            data: MenuUpdate
    ) -> models.Menu | None:
        """Update exist menu."""
        menu = await self._get_from_db(menu_id)

        if menu:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(menu, key, value)
            self.session.add(menu)
            await self.session.commit()

        return menu

    async def delete(self, menu_id: uuid.UUID) -> models.Menu | None:
        """Delete exist menu."""
        menu = await self._get_from_db(menu_id)

        if menu:
            await self.session.delete(menu)
            await self.session.commit()

        return menu


async def get_menu_repo(
        session: AsyncSession = Depends(get_db)
) -> MenuRepository:
    """Instance of MenuRepository."""
    return MenuRepository(session=session)
