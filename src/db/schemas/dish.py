import decimal
import uuid

from pydantic import BaseModel, Field


class DishCreate(BaseModel):
    """Create dish schema."""
    title: str = Field(min_length=3)
    description: str | None = None
    price: decimal.Decimal = Field(ge=0)


class DishUpdate(BaseModel):
    """Update dish schema."""
    title: str | None = Field(min_length=3, default=None)
    description: str | None = None
    price: decimal.Decimal | None = Field(ge=0, default=None)


class DishResponse(BaseModel):
    """Response dish schema."""
    id: uuid.UUID
    title: str
    description: str
    price: decimal.Decimal

    class ConfigDict:
        from_attributes = True
