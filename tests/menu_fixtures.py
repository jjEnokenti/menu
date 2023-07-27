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


@pytest.fixture
async def menus_list_response(
        get_app: FastAPI,
        client: AsyncClient
) -> Response:
    """Request to return the list of menus."""

    url = get_app.url_path_for('get_list_menu')
    menus = await client.get(url, follow_redirects=True)

    return menus


@pytest.fixture
async def get_menu_id(menus_list_response: Response) -> uuid.UUID:
    """Pars id from first menu in menu list."""

    return menus_list_response.json()[0].get('id')


@pytest.fixture
async def create_menu_response(
        get_app: FastAPI,
        client: AsyncClient,
        create_menu_data: Dict[str, Union[str, int, uuid.UUID]]
) -> Response:
    """Request to create a menu."""

    url = get_app.url_path_for('create_menu')
    menu = await client.post(
        url,
        json=create_menu_data,
        follow_redirects=True
    )

    return menu


@pytest.fixture
async def detail_menu_response(
        client: AsyncClient,
        get_menu_id: uuid.UUID,
        get_app: FastAPI
) -> Response:
    """Request to return the detail of menu."""

    url = get_app.url_path_for('get_detail_menu', menu_id=get_menu_id)
    menu = await client.get(url)

    return menu


@pytest.fixture
async def update_menu_response(
        client: AsyncClient,
        get_menu_id: uuid.UUID,
        get_app: FastAPI,
        update_menu_data: Dict[str, Union[str, int, uuid.UUID]]
) -> Response:
    """Request to update the detail of menu."""

    url = get_app.url_path_for('update_menu', menu_id=get_menu_id)
    menu = await client.patch(
        url,
        json=update_menu_data,
        follow_redirects=True
    )

    return menu


@pytest.fixture
async def delete_menu_response(
        client: AsyncClient,
        get_menu_id: uuid.UUID,
        get_app: FastAPI
) -> Response:
    """Request to delete menu."""

    url = get_app.url_path_for('delete_menu', menu_id=get_menu_id)
    menu = await client.delete(url, follow_redirects=True)

    return menu


@pytest.fixture
async def non_existent_menu_response(
        client: AsyncClient,
        get_app: FastAPI
) -> Response:
    """Request to get a non-existent menu."""

    url = get_app.url_path_for(
        'get_detail_menu',
        menu_id='5372d4ba-1e98-4b37-b1fe-000000000000'
    )
    menu = await client.get(url, follow_redirects=True)

    return menu


@pytest.fixture
def response_menu_data(
        get_menu_id: uuid.UUID
) -> Dict[str, Union[str, int, uuid.UUID]]:
    """Response data of menu."""

    return {
        'id': get_menu_id,
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 0,
        'dishes_count': 0
    }


@pytest.fixture
def create_menu_data() -> Dict[str, str]:
    """Data for create of menu."""

    return {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }


@pytest.fixture
def update_menu_data() -> Dict[str, str]:
    """Data for update of menu."""

    return {
        'title': 'My updated menu',
        'description': 'My updated menu description'
    }
