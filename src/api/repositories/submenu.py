import uuid
from typing import Sequence

from sqlalchemy import Row, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.repositories.abstract_repository import AbstractRepository
from src.db import models

__all__ = (
    'SubmenuRepository',
)


class SubmenuRepository(AbstractRepository):
    """Submenu repository."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = models.Submenu
        self.dish_model = models.Dish

    def get_statement(self, menu_id: uuid.UUID) -> Select:
        """Get statement for execute from DB."""

        return select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.menu_id,
            func.count(self.model.dishes).label('dishes_count'),
        ).join(
            self.dish_model,
            self.model.id == self.dish_model.submenu_id,
            isouter=True
        ).group_by(
            self.model.id
        ).where(self.model.menu_id == menu_id)

    async def get_detail(
            self,
            submenu_id: uuid.UUID,
            menu_id: uuid.UUID,
    ) -> Row | None:
        """Get detail of submenu from DB."""

        result = await self.session.execute(
            statement=self.get_statement(menu_id).where(self.model.id == submenu_id)
        )

        return result.first()

    async def get_list(self, menu_id: uuid.UUID) -> Sequence[Row]:
        """Get list of submenu from DB."""

        result = await self.session.execute(
            statement=self.get_statement(menu_id)
        )

        return result.all()

    async def create(self, data: dict, **kwargs) -> models.Submenu:
        """Create new submenu."""

        submenu = self.model(**data, **kwargs)

        self.session.add(submenu)

        return submenu

    async def update(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: dict,
    ) -> models.Submenu | None:
        """Update submenu."""

        submenu = await self._get_from_db(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )

        for key, value in data.items():
            setattr(submenu, key, value)
        self.session.add(submenu)

        return submenu

    async def delete(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
    ) -> bool:
        """Delete submenu."""

        submenu = await self._get_from_db(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )

        if submenu:
            await self.session.delete(submenu)
            return True

        return False

    async def _get_from_db(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
    ) -> models.Submenu | None:
        """Get submenu from DB for delete/update."""

        result = await self.session.execute(
            select(
                self.model
            ).options(
                joinedload(self.model.dishes)
            ).where(
                self.model.menu_id == menu_id,
                self.model.id == submenu_id,
            )
        )

        return result.unique().scalar_one_or_none()
