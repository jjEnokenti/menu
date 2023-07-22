from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from src.config import settings


__all__ = (
    'engine',
    'session',
    'get_db',
)

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
    future=True
)

session = AsyncSession(
    bind=engine,
    expire_on_commit=False
)


async def get_db(request: Request):
    """Get DB session."""
    return request.state.db
