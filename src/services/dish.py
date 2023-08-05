import uuid

from fastapi import Depends, HTTPException, status

from src.cache.cache import Cache, get_cache
from src.db import models
from src.db.schemas import Status
from src.db.schemas import dish as dish_schemas
from src.repositories.dish import DishRepository, get_dish_repo
from src.services.abstract_service import AbstractService


class DishService(AbstractService):
    """Service layer."""

    def __init__(self, repo: DishRepository, cache: Cache):
        self.repo = repo
        self.cache = cache

    async def get_detail(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID
    ) -> dict:
        """Get detail of dish from cache DB layer."""
        dish = await self.get_obj_from_cache(
            self.detail_dish.format(menu_id, submenu_id, dish_id)
        )

        if not dish:
            try:
                dish = await self.repo.get_detail(dish_id)
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )

        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )

        await self.cache_invalidate(
            self.detail_dish.format(menu_id, submenu_id, dish_id),
            dish
        )

        return dish

    async def get_list(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID
    ) -> list:
        """Get list of dishes from cache or DB layer."""

        dishes = await self.get_obj_from_cache(
            self.dishes_list.format(menu_id, submenu_id)
        )

        if not dishes:
            try:
                dishes = await self.repo.get_list(submenu_id)
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )

            if dishes:
                await self.cache_invalidate(
                    self.dishes_list.format(menu_id, submenu_id),
                    dishes
                )

        return dishes

    async def create(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: dish_schemas.DishCreate
    ) -> models.Dish | None:
        """Create new dish logic and remove from cache."""
        try:
            async with self.repo.session.begin():
                new_dish = await self.repo.create(submenu_id=submenu_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        await self.cache_invalidate(
            self.dishes_list.format(menu_id, submenu_id),
            self.detail_submenu.format(menu_id, submenu_id),
            self.submenus_list.format(menu_id),
            self.detail_menu.format(menu_id),
            self.menus_list
        )

        return new_dish

    async def update(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            data: dish_schemas.DishUpdate
    ) -> models.Dish | None:
        """Update dish logic and remove from cache."""
        try:
            async with self.repo.session.begin():
                dish = await self.repo.update(dish_id=dish_id, data=data)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )
        await self.cache_invalidate(
            self.dishes_list.format(menu_id, submenu_id),
            self.detail_dish.format(menu_id, submenu_id, dish_id)
        )

        return dish

    async def delete(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID
    ) -> Status:
        """Delete dish logic and remove from cache."""
        try:
            async with self.repo.session.begin():
                deleted_dish = await self.repo.delete(dish_id)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if not deleted_dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )

        await self.cache_invalidate(
            self.dishes_list.format(menu_id, submenu_id),
            self.detail_dish.format(menu_id, submenu_id, dish_id),
            self.detail_submenu.format(menu_id, submenu_id),
            self.submenus_list.format(menu_id),
            self.detail_menu.format(menu_id),
            self.menus_list
        )

        return Status(message=f'Dish {dish_id} was successfully deleted!')


async def get_dish_service(
        repo: DishRepository = Depends(get_dish_repo),
        cache: Cache = Depends(get_cache)
) -> DishService:
    """Instance of DishService."""
    return DishService(repo=repo, cache=cache)
