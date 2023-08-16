import uuid
from functools import partial
from typing import Sequence

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import Row

from src.api import keys_for_cache_invalidation
from src.api.repositories.dish import DishRepository
from src.api.schemas import DishCreate, DishUpdate, Status
from src.api.services.utils import set_discount, set_discounts
from src.cache.service import CacheService
from src.db import models


class DishService:
    """Dish service layer."""

    def __init__(self, repo: DishRepository, cache: CacheService):
        self.repo = repo
        self.cache = cache

    async def get_detail(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
    ) -> Sequence | dict | None:
        """Get detail of dish from cache DB."""

        dish = await self.cache.get_obj_from_cache(
            keys_for_cache_invalidation.DETAIL_DISH.format(menu_id, submenu_id, dish_id),
        )

        if not dish:
            try:
                dish = await self.repo.get_detail(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish_id=dish_id,
                )
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )

            if dish:
                discount = await self.cache.get_discount(dish_id)
                if discount:
                    dish = await set_discount(dish, discount)

                await self.cache.set_value_into_cache(
                    keys_for_cache_invalidation.DETAIL_DISH.format(menu_id, submenu_id, dish_id),
                    dish,
                )

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='dish not found'
                )

        return dish

    async def get_list(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
    ) -> Sequence[Row]:
        """Get list of dishes from cache or DB."""

        dishes = await self.cache.get_obj_from_cache(
            keys_for_cache_invalidation.DISHES_LIST.format(menu_id, submenu_id)
        )

        if not dishes:
            try:
                dishes = await self.repo.get_list(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                )
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error.args
                )

            if dishes:

                discounts = await self.cache.get_discounts()
                if discounts:
                    dishes = await set_discounts(discounts, dishes)

                await self.cache.set_value_into_cache(
                    keys_for_cache_invalidation.DISHES_LIST.format(menu_id, submenu_id),
                    dishes,
                )

        return dishes

    async def create(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: DishCreate,
            background_tasks: BackgroundTasks,
    ) -> models.Dish:
        """Create new dish and invalidate cache."""

        try:
            async with self.repo.session.begin():
                new_dish = await self.repo.create(
                    data=data.model_dump(),
                    submenu_id=submenu_id,
                )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        background_tasks.add_task(
            partial(
                self.cache.cache_invalidate,
                keys_for_cache_invalidation.DISHES_LIST.format(menu_id, submenu_id),
                keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, submenu_id),
                keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id),
                keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
                keys_for_cache_invalidation.MENUS_LIST,
            )
        )

        return new_dish

    async def update(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            data: DishUpdate,
            background_tasks: BackgroundTasks,
    ) -> models.Dish | None:
        """Update dish and invalidate cache."""

        try:
            async with self.repo.session.begin():
                dish = await self.repo.update(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish_id=dish_id,
                    data=data.model_dump(exclude_unset=True),
                )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if dish:
            background_tasks.add_task(
                partial(
                    self.cache.cache_invalidate,
                    keys_for_cache_invalidation.DISHES_LIST.format(menu_id, submenu_id),
                    keys_for_cache_invalidation.DETAIL_DISH.format(menu_id, submenu_id, dish_id),
                )
            )

            return dish

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )

    async def delete(
            self,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            dish_id: uuid.UUID,
            background_tasks: BackgroundTasks,
    ) -> Status:
        """Delete dish and invalidate cache."""

        try:
            async with self.repo.session.begin():
                deleted_dish = await self.repo.delete(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish_id=dish_id,
                )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error.args
            )

        if deleted_dish:
            background_tasks.add_task(
                partial(
                    self.cache.cache_invalidate,
                    keys_for_cache_invalidation.DISHES_LIST.format(menu_id, submenu_id),
                    keys_for_cache_invalidation.DETAIL_DISH.format(menu_id, submenu_id, dish_id),
                    keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, submenu_id),
                    keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id),
                    keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
                    keys_for_cache_invalidation.MENUS_LIST,
                )
            )

            return Status(status=f'Dish {dish_id} was successfully deleted!')

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )
