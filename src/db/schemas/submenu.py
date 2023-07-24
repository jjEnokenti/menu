import uuid
from typing import Optional

from pydantic import BaseModel


class SubmenuCreate(BaseModel):
    """Create submenu schema."""
    title: str
    description: str


class SubmenuUpdate(BaseModel):
    """Update submenu schema."""
    title: Optional[str]
    description: Optional[str]


class SubmenuResponse(BaseModel):
    """Response submenu schema."""
    id: uuid.UUID
    title: str
    description: str
    menu_id: uuid.UUID
    dishes_count: int = 0

    class ConfigDict:
        from_attributes = True
