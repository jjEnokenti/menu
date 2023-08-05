import uuid

from pydantic import BaseModel, Field


class SubmenuCreate(BaseModel):
    """Create submenu schema."""
    title: str = Field(min_length=3)
    description: str | None = None


class SubmenuUpdate(BaseModel):
    """Update submenu schema."""
    title: str | None = Field(min_length=3, default=None)
    description: str | None = None


class SubmenuResponse(BaseModel):
    """Response submenu schema."""
    id: uuid.UUID
    title: str
    description: str
    menu_id: uuid.UUID
    dishes_count: int = 0

    class ConfigDict:
        from_attributes = True
