from pydantic import BaseModel


class Status(BaseModel):
    """Response status schema."""
    message: str
