import decimal
import uuid
from typing import Optional

from pydantic import BaseModel


class DishCreate(BaseModel):
    """Create dish schema."""
    title: str
    description: str
    price: decimal.Decimal


class DishUpdate(BaseModel):
    """Update dish schema."""
    title: Optional[str]
    description: Optional[str]
    price: Optional[decimal.Decimal]


class DishResponse(BaseModel):
    """Response dish schema."""
    id: uuid.UUID
    title: str
    description: str
    price: decimal.Decimal

    class ConfigDict:
        from_attributes = True
