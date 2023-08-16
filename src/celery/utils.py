import copy
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api import keys_for_cache_invalidation
from src.cache.service import CacheService
from src.db import models


class Synchronizer:

    def __init__(self, excel_data, session: AsyncSession, cache: CacheService):
        self.session = session
        self.excel_data = excel_data
        self.cache = cache

        self.excel_menus: dict[str, dict] = {}
        self.excel_submenus: dict[str, dict] = {}
        self.excel_dishes: dict[str, dict] = {}

        self.db_menus: dict[str, dict] = {}
        self.db_submenus: dict[str, dict] = {}
        self.db_dishes: dict[str, dict] = {}

        self.menus_for_update: list[dict] = []
        self.submenus_for_update: list[dict] = []
        self.dishes_for_update: list[dict] = []

        self.discount_prices: list[tuple] = []

        self.discounts: dict[str, str] = {}

        self.invalidate_keys: list[str] = []

    async def setup(self) -> None:
        """Checking data for changes and further synchronizing them."""

        async with self.session.begin():
            db_data = [item.as_dict() for item in await self.db_data()]

            self.discounts = await self.cache.get_discounts()

            await self.parser_data(db_data, is_db=True)
            await self.parser_data(self.excel_data)

            if db_data == self.excel_data and not self.discount_prices and not self.invalidate_keys:
                return None

            await self.create_items()
            await self.delete_items()
            await self.update_items()

            if self.invalidate_keys:
                await self.cache.cache_invalidate(*self.invalidate_keys)

            if self.discount_prices:
                for discount in self.discount_prices:
                    await self.cache.set_value_into_cache(key=discount[0], value=discount[1], ex=3600)

    async def db_data(self) -> Sequence:
        """Get all data."""

        items = await self.session.execute(
            select(
                models.Menu
            ).options(
                joinedload(models.Menu.submenus).joinedload(models.Submenu.dishes)
            )
        )

        return items.scalars().unique().all()

    async def update_items(self) -> None:
        """Update items from excel data."""

        self.data_for_update()

        if self.menus_for_update:
            for menu in self.menus_for_update:
                stmt = update(models.Menu).where(models.Menu.id == menu['id']).values(**menu)
                await self.session.execute(stmt)
                self.invalidate_keys.extend(
                    [
                        keys_for_cache_invalidation.MENUS_LIST,
                        keys_for_cache_invalidation.DETAIL_MENU.format(menu['id']),
                    ]
                )

        if self.submenus_for_update:
            for submenu in self.submenus_for_update:
                stmt = update(models.Submenu).where(models.Submenu.id == submenu['id']).values(**submenu)
                await self.session.execute(stmt)
                self.invalidate_keys.extend(
                    [
                        keys_for_cache_invalidation.DETAIL_SUBMENU.format(submenu['menu_id'], submenu['id']),
                        keys_for_cache_invalidation.SUBMENUS_LIST.format(submenu['menu_id']),
                    ]
                )

        if self.dishes_for_update:
            for dish in self.dishes_for_update:
                menu_id = dish.pop('menu_id')
                stmt = update(models.Dish).where(models.Dish.id == dish['id']).values(**dish)
                await self.session.execute(stmt)
                self.invalidate_keys.extend(
                    [
                        keys_for_cache_invalidation.DISHES_LIST.format(menu_id, dish['submenu_id']),
                        keys_for_cache_invalidation.DETAIL_DISH.format(menu_id, dish['submenu_id'], dish['id']),
                    ]
                )

    async def create_items(self) -> None:
        """Create new items in db."""

        for menu in self.excel_menus:
            if menu not in self.db_menus:
                self.session.add(models.Menu(**self.excel_menus[menu]))
                self.invalidate_keys.append(keys_for_cache_invalidation.MENUS_LIST)

        for submenu in self.excel_submenus:
            if submenu not in self.db_submenus:
                menu_id = self.excel_submenus[submenu]['menu_id']
                self.session.add(models.Submenu(**self.excel_submenus[submenu]))
                self.invalidate_keys.extend([
                    keys_for_cache_invalidation.MENUS_LIST,
                    keys_for_cache_invalidation.DETAIL_MENU.format(menu_id)]
                )

        for dish in self.excel_dishes:
            if dish not in self.db_dishes:
                new_dish = copy.deepcopy(self.excel_dishes[dish])
                menu_id = new_dish.pop('menu_id')
                self.session.add(models.Dish(**new_dish))
                self.invalidate_keys.extend(
                    [
                        keys_for_cache_invalidation.DISHES_LIST.format(menu_id, new_dish['submenu_id']),
                        keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, new_dish['submenu_id']),
                        keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id),
                        keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
                        keys_for_cache_invalidation.MENUS_LIST,
                    ]
                )

    async def delete_items(self) -> None:
        """Start deleting objects if such exist."""

        menu_for_delete_id = self.ids_to_delete_or_create(
            self._get_ids(self.db_menus), self._get_ids(self.excel_menus)
        )
        submenu_for_delete_id = self.ids_to_delete_or_create(
            self._get_ids(self.db_submenus), self._get_ids(self.excel_submenus)
        )
        dish_for_delete_id = self.ids_to_delete_or_create(
            self._get_ids(self.db_dishes), self._get_ids(self.excel_dishes)
        )

        if menu_for_delete_id:
            menus = await self.get_objects(menu_for_delete_id, models.Menu)

            for menu in menus:
                await self.session.delete(menu)
                await self.cache.cache_invalidate(
                    keys_for_cache_invalidation.MENUS_LIST,
                    keys_for_cache_invalidation.DETAIL_MENU.format(menu.id),
                    invalid_key=menu.id,
                )

            return None

        if submenu_for_delete_id:
            submenus = await self.get_objects(submenu_for_delete_id, models.Submenu)

            for submenu in submenus:
                await self.session.delete(submenu)
                await self.cache.cache_invalidate(
                    keys_for_cache_invalidation.DETAIL_SUBMENU.format(submenu.menu_id, submenu.id),
                    keys_for_cache_invalidation.SUBMENUS_LIST.format(submenu.menu_id),
                    keys_for_cache_invalidation.MENUS_LIST,
                    keys_for_cache_invalidation.DETAIL_MENU.format(submenu.menu_id),
                    invalid_key=submenu.id,
                )

            return None

        if dish_for_delete_id:
            dishes = [self.db_dishes[dish_id] for dish_id in dish_for_delete_id]

            for dish in dishes:
                menu_id = dish['menu_id']
                dish_entity: type[models.Dish] | None = await self.session.get(models.Dish, dish['id'])

                await self.session.delete(dish_entity)
                await self.cache.cache_invalidate(
                    keys_for_cache_invalidation.DISHES_LIST.format(menu_id, dish['submenu_id']),
                    keys_for_cache_invalidation.DETAIL_DISH.format(menu_id, dish['submenu_id'], dish['id']),
                    keys_for_cache_invalidation.DETAIL_SUBMENU.format(menu_id, dish['submenu_id']),
                    keys_for_cache_invalidation.SUBMENUS_LIST.format(menu_id),
                    keys_for_cache_invalidation.DETAIL_MENU.format(menu_id),
                    keys_for_cache_invalidation.MENUS_LIST,
                )

    async def get_objects(self, ids, model):
        """Get objects from db by ids."""

        query = await self.session.execute(
            select(model).filter(model.id.in_(ids))
        )

        return query.scalars().unique().all()

    async def parser_data(self, data: list, is_db=False) -> None:
        """Parse data to separation of entities into separate variables."""

        for menu in data:
            submenus = menu.pop('submenus', [])
            if is_db:
                self.db_menus[menu['id']] = menu
            else:
                self.excel_menus[menu['id']] = menu

            for submenu in submenus:
                submenu['menu_id'] = menu['id']
                dishes = submenu.pop('dishes', [])
                if is_db:
                    self.db_submenus[submenu['id']] = submenu
                else:
                    self.excel_submenus[submenu['id']] = submenu

                for dish in dishes:
                    dish['submenu_id'] = submenu['id']
                    dish['menu_id'] = menu['id']

                    if is_db:
                        self.db_dishes[dish['id']] = dish
                        continue

                    key = f'discount:{dish["id"]}'
                    inv_keys = await self.cache.get_keys_by_pattern(menu['id'])

                    if 'discount' in dish:

                        if dish['discount'] != self.discounts.get(key):
                            self.discount_prices.append((key, dish['discount']))
                            self.invalidate_keys.extend([
                                keys_for_cache_invalidation.DETAIL_DISH.format(
                                    menu['id'], submenu['id'], dish['id']
                                ),
                                keys_for_cache_invalidation.DISHES_LIST.format(
                                    menu['id'], submenu['id']
                                ),
                                *inv_keys
                            ])
                        dish.pop('discount')

                    else:
                        if key in self.discounts:
                            self.invalidate_keys.extend([
                                key,
                                *inv_keys
                            ])

                    self.excel_dishes[dish['id']] = dish

    def data_for_update(self):
        """Prepare items for update."""

        for menu in self.excel_menus:
            if menu in self.db_menus and self.excel_menus[menu] != self.db_menus[menu]:
                self.menus_for_update.append(self.excel_menus[menu])

        for submenu in self.excel_submenus:
            if submenu in self.db_submenus and self.excel_submenus[submenu] != self.db_submenus[submenu]:
                self.submenus_for_update.append(self.excel_submenus[submenu])

        for dish in self.excel_dishes:
            if dish in self.db_dishes and self.excel_dishes[dish] != self.db_dishes[dish]:
                self.dishes_for_update.append(self.excel_dishes[dish])

    @staticmethod
    def _get_ids(seq) -> list:
        """get list of ids of entities"""
        return [key for key in seq.keys()]

    @staticmethod
    def ids_to_delete_or_create(lst_ids_1, lst_ids_2, create=False) -> set:
        """Get set object IDs to delete/create."""
        if create:
            return set(lst_ids_2) - set(lst_ids_1)

        return set(lst_ids_1) - set(lst_ids_2)
