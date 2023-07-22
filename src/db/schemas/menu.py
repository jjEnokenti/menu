import uuid
from typing import (
    List,
    Optional,
    Type,
)

from pydantic import BaseModel

from src.db.models import Submenu


class MenuBase(BaseModel):
    """Base menu schema."""
    title: str
    description: str
    submenus: Optional[List[Type[Submenu]]] | None = None


class MenuCreate(MenuBase):
    """Create menu schema."""
    title: str
    description: str


class MenuUpdate(BaseModel):
    """Update menu schema."""
    title: str | None = None
    description: str | None = None


class MenuInDB(MenuBase):
    """Menu schema in DB."""
    id: uuid.UUID


class MenuResponse(BaseModel):
    """Menu response schema."""
    id: uuid.UUID
    title: str
    description: str
    quantity_submenu: int = 0
    quantity_dish: int = 0

    class Config:
        from_attributes = True


class Status(BaseModel):
    """Response status schema."""
    message: str
