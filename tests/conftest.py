import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from src.app import app
from src.config import test_settings
from src.db.core import get_db
from src.db.models import Base


async_test_engine = create_async_engine(
    url=test_settings.DATABASE_URL,
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


@pytest.fixture(autouse=True, scope='module')
async def prepare_database():
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


@pytest.fixture
def create_menu_data():
    return {
        'title': 'Menu 1',
        'description': 'Menu description 1'
    }


@pytest.fixture
def create_submenu_data():
    return {
        'title': 'Submenu 1',
        'description': 'Submenu description 1'
    }


@pytest.fixture
def create_dish_data():
    return {
        'title': 'Dish 1',
        'description': 'Dish description 1',
        'price': '100.50',
    }


@pytest.fixture
def update_menu_data():
    return {
        'title': 'Updated menu',
        'description': 'Updated menu description'
    }


@pytest.fixture
def update_submenu_data():
    return {
        'title': 'Updated submenu',
        'description': 'Updated submenu description'
    }


@pytest.fixture
def update_dish_data():
    return {
        'title': 'Updated dish',
        'description': 'Updated dish description',
        'price': '999.99',
    }
