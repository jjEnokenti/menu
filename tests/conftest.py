import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from src.app import app
from src.config import settings
from src.db.core import get_db
from src.db.models import Base


pytest_plugins = (
    'tests.menu_fixtures,'
    'tests.submenu_fixtures,'
    'tests.dish_fixtures'
)

async_test_engine = create_async_engine(
    url=settings.DATABASE_URL,
)

async_test_session = AsyncSession(
    bind=async_test_engine,
    expire_on_commit=False
)

Base.metadata.bind = async_test_engine


async def override_get_db():
    async with async_test_session as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='class')
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='class')
async def client():
    async with AsyncClient(app=app, base_url='http://test') as cl:
        yield cl


@pytest.fixture
def get_app():
    return app
