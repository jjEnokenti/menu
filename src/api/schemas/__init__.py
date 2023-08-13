import decimal
import uuid

from pydantic import BaseModel
from .menu import MenuCreate, MenuUpdate, MenuResponse
from .submenu import SubmenuCreate, SubmenuUpdate, SubmenuResponse
from .dish import DishCreate, DishUpdate, DishResponse

__all__ = (
    'Status',
    'MenuInDB',
    'MenuCreate',
    'MenuUpdate',
    'MenuResponse',
    'SubmenuCreate',
    'SubmenuUpdate',
    'SubmenuResponse',
    'DishCreate',
    'DishUpdate',
    'DishResponse',
)


class Status(BaseModel):
    """Response status schema."""
    status: str


class BaseEntity(BaseModel):
    """Base entity schema in DB."""
    id: uuid.UUID
    title: str
    description: str | None = None
    #
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "id": "6fa85f64-5717-4562-b3fc-2c963f66afa2",
    #                 "title": "Menu title",
    #                 "description": "Menu description",
    #                 "submenus": [
    #                     {
    #                         "id": "1fa85f64-5717-4562-b3fc-2c963f66afa3",
    #                         "title": "Submenu title",
    #                         "description": "Submenu description",
    #                         "dishes": [
    #                             {
    #                                 "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #                                 "title": "Dish title",
    #                                 "description": "Dish description",
    #                                 "price": 100.50
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # }


class DishesInDB(BaseEntity):
    price: decimal.Decimal


class SubmenuInDB(BaseEntity):
    dishes: list[DishesInDB]


class MenuInDB(BaseEntity):
    submenus: list[SubmenuInDB]
