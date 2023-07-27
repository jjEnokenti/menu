import uuid
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class SubmenuCreate(BaseModel):
    """Create submenu schema."""
    title: str = Field(min_length=3)
    description: str


class SubmenuUpdate(BaseModel):
    """Update submenu schema."""
    title: Optional[str] = Field(min_length=3)
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
