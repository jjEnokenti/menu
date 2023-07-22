import uuid
from typing import Optional

from pydantic import BaseModel


class MenuCreate(BaseModel):
    """Create menu schema."""
    title: str
    description: str


class MenuUpdate(BaseModel):
    """Update menu schema."""
    title: Optional[str]
    description: Optional[str]


class MenuResponse(BaseModel):
    """Menu response schema."""
    id: uuid.UUID
    title: str
    description: str
    quantity_submenu: int = 0
    quantity_dish: int = 0

    class Config:
        from_attributes = True
