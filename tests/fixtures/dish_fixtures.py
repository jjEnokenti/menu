import uuid
from typing import (
    Dict,
    Union,
)

import pytest
from fastapi import FastAPI
from httpx import (
    AsyncClient,
    Response,
)
from pytest_asyncio.plugin import SubRequest


@pytest.fixture
async def dish_list_response(
        get_app: FastAPI,
        client: AsyncClient,
        get_submenu_id: uuid.UUID,
        get_menu_id: uuid.UUID
) -> Response:
    """Request to return the list of dishes."""

    url = get_app.url_path_for(
        'get_list_dish',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id
    )
    dishes = await client.get(url, follow_redirects=True)

    return dishes


@pytest.fixture
async def get_dish_id(dish_list_response: Response) -> uuid.UUID:
    """Pars id from first dish in list of dishes."""
    dishes = dish_list_response.json()

    if dishes:
        return dishes[-1].get('id')

    return uuid.uuid4()


@pytest.fixture
async def create_dish_response(
        get_app: FastAPI,
        client: AsyncClient,
        get_submenu_id: uuid.UUID,
        get_menu_id: uuid.UUID,
        request: SubRequest,
) -> Response:
    """Request to create a dish."""

    data = request.getfixturevalue(request.param)

    url = get_app.url_path_for(
        'create_dish',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id
    )

    dish = await client.post(
        url,
        json=data,
        follow_redirects=True
    )

    return dish


@pytest.fixture
async def detail_dish_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID,
        get_submenu_id: uuid.UUID,
        get_dish_id: uuid.UUID
) -> Response:
    """Request to return the detail of dish."""

    url = get_app.url_path_for(
        'get_detail_dish',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id,
        dish_id=get_dish_id
    )
    dish = await client.get(url, follow_redirects=True)

    return dish


@pytest.fixture
async def update_dish_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID,
        get_submenu_id: uuid.UUID,
        get_dish_id: uuid.UUID,
        update_dish_data: Dict[str, str]
) -> Response:
    """Request to update the detail of dish."""

    url = get_app.url_path_for(
        'update_dish',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id,
        dish_id=get_dish_id
    )
    dish = await client.patch(
        url,
        json=update_dish_data,
        follow_redirects=True
    )

    return dish


@pytest.fixture
async def delete_dish_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID,
        get_submenu_id: uuid.UUID,
        get_dish_id: uuid.UUID
) -> Response:
    """Request to delete dish."""

    url = get_app.url_path_for(
        'delete_dish',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id,
        dish_id=get_dish_id
    )
    dish = await client.delete(url, follow_redirects=True)

    return dish


@pytest.fixture
async def non_existent_dish_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID,
        get_submenu_id: uuid.UUID
) -> Response:
    """Request to get a non-existent dish."""

    url = get_app.url_path_for(
        'get_detail_dish',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id,
        dish_id='5372d4ba-1e98-4b37-b1fe-000000000000'
    )
    dish = await client.get(url, follow_redirects=True)

    return dish


@pytest.fixture
def response_dish_data(
        get_dish_id: uuid.UUID,
        dish_list_response: Response,
) -> Dict[str, Union[str, int, uuid.UUID]]:
    """Response data of dish."""

    return {
        'id': get_dish_id,
        'title': dish_list_response.json()[-1].get('title'),
        'description': dish_list_response.json()[-1].get('description'),
        'price': dish_list_response.json()[-1].get('price')
    }


@pytest.fixture
def create_dish_data() -> Dict[str, str]:
    """Data for create of dish."""

    return {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '100.50'
    }


@pytest.fixture
def create_dish_data_second() -> Dict[str, str]:
    """Data for create of second dish."""

    return {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '15.50'
    }


@pytest.fixture
def update_dish_data() -> Dict[str, str]:
    """Data for update of dish."""

    return {
        'title': 'My updated dish',
        'description': 'My updated dish description',
        'price': '999.99'
    }
