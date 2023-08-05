import uuid

from pydantic import BaseModel, Field


class MenuCreate(BaseModel):
    """Create menu schema."""
    title: str = Field(min_length=3)
    description: str | None = None


class MenuUpdate(BaseModel):
    """Update menu schema."""
    title: str | None = Field(min_length=3, default=None)
    description: str | None = None


class MenuResponse(BaseModel):
    """Menu response schema."""
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

    class ConfigDict:
        from_attributes = True
