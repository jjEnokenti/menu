import uuid
from typing import Sequence

from fastapi import Depends
from sqlalchemy import Row, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models
from src.db.core import get_db
from src.db.schemas.submenu import SubmenuCreate, SubmenuUpdate
from src.repositories.abstract_repository import AbstractRepository

__all__ = (
    'SubmenuRepository',
    'get_submenu_repo',
)


class SubmenuRepository(AbstractRepository):
    """Database layer."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_statement(self) -> Select:
        """Get statement for execute from DB."""
        return select(
            self.submenu_model.id,
            self.submenu_model.title,
            self.submenu_model.description,
            self.submenu_model.menu_id,
            func.count(self.submenu_model.dishes).label('dishes_count')
        ).join(
            self.dish_model,
            self.submenu_model.id == self.dish_model.submenu_id,
            isouter=True
        ).group_by(
            self.submenu_model.id
        )

    async def _get_from_db(self, submenu_id: uuid.UUID) -> models.Submenu | None:
        """Get submenu for delete/update from DB."""
        stmt = select(
            self.submenu_model
        ).where(self.submenu_model.id == submenu_id)

        result = await self.session.execute(
            statement=stmt
        )

        return result.scalar_one_or_none()

    async def get_detail(self, submenu_id: uuid.UUID) -> models.Submenu | None:
        """Get detail of submenu from DB."""
        stmt = self.get_statement().where(self.submenu_model.id == submenu_id)

        result = await self.session.execute(
            statement=stmt
        )

        return result.first()

    async def get_list(self, menu_id: uuid.UUID) -> Sequence[Row]:
        """Get list of submenu from DB."""
        stmt = self.get_statement().where(
            self.submenu_model.menu_id == menu_id
        )

        result = await self.session.execute(
            statement=stmt
        )

        return result.all()

    async def create(self, menu_id: uuid.UUID, data: SubmenuCreate) -> models.Submenu:
        """Create new submenu."""
        new_submenu = self.submenu_model(
            **data.model_dump(exclude_unset=True),
            menu_id=menu_id
        )

        self.session.add(new_submenu)

        return new_submenu

    async def update(
            self,
            submenu_id: uuid.UUID,
            data: SubmenuUpdate
    ) -> models.Submenu | None:
        """Update exist submenu."""
        submenu = await self._get_from_db(submenu_id)

        if submenu:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(submenu, key, value)
            self.session.add(submenu)
            await self.session.commit()

        return submenu

    async def delete(self, submenu_id: uuid.UUID) -> models.Submenu | None:
        """Delete exist menu."""
        submenu = await self._get_from_db(submenu_id)

        if submenu:
            await self.session.delete(submenu)
            await self.session.commit()

        return submenu


async def get_submenu_repo(
        session: AsyncSession = Depends(get_db)
) -> SubmenuRepository:
    """Instance of SubmenuRepository."""
    return SubmenuRepository(session=session)
