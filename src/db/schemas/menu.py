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
    submenus_count: int = 0
    dishes_count: int = 0

    class ConfigDict:
        from_attributes = True
