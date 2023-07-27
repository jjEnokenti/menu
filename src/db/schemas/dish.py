import decimal
import uuid
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class DishCreate(BaseModel):
    """Create dish schema."""
    title: str = Field(min_length=3)
    description: str
    price: decimal.Decimal = Field(ge=0)


class DishUpdate(BaseModel):
    """Update dish schema."""
    title: Optional[str] = Field(min_length=3)
    description: Optional[str]
    price: Optional[decimal.Decimal] = Field(ge=0)


class DishResponse(BaseModel):
    """Response dish schema."""
    id: uuid.UUID
    title: str
    description: str
    price: decimal.Decimal

    class ConfigDict:
        from_attributes = True
