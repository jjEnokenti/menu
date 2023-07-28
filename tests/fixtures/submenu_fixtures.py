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
async def submenus_list_response(
        get_app: FastAPI,
        client: AsyncClient,
        get_menu_id: uuid.UUID
) -> Response:
    """Request to return the list of submenus."""

    url = get_app.url_path_for('get_list_submenu', menu_id=get_menu_id)
    submenus = await client.get(url, follow_redirects=True)

    return submenus


@pytest.fixture
async def get_submenu_id(submenus_list_response: Response) -> uuid.UUID:
    """Pars id from first submenu in submenu list."""

    return submenus_list_response.json()[0].get('id')


@pytest.fixture
async def create_submenu_response(
        get_app: FastAPI,
        client: AsyncClient,
        get_menu_id: uuid.UUID,
        create_submenu_data: Dict[str, str]
) -> Response:
    """Request to create a submenu."""

    url = get_app.url_path_for('create_submenu', menu_id=get_menu_id)
    submenu = await client.post(
        url,
        json=create_submenu_data,
        follow_redirects=True
    )

    return submenu


@pytest.fixture
async def detail_submenu_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID,
        get_submenu_id: uuid.UUID
) -> Response:
    """Request to return the detail of submenu."""

    url = get_app.url_path_for(
        'get_detail_submenu',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id
    )
    submenu = await client.get(url, follow_redirects=True)

    return submenu


@pytest.fixture
async def update_submenu_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID,
        get_submenu_id: uuid.UUID,
        update_submenu_data: Dict[str, str]
) -> Response:
    """Request to update the detail of submenu."""

    url = get_app.url_path_for(
        'update_submenu',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id
    )
    submenu = await client.patch(
        url,
        json=update_submenu_data,
        follow_redirects=True
    )

    return submenu


@pytest.fixture
async def delete_submenu_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID,
        get_submenu_id: uuid.UUID
) -> Response:
    """Request to delete submenu."""

    url = get_app.url_path_for(
        'delete_submenu',
        menu_id=get_menu_id,
        submenu_id=get_submenu_id
    )
    submenu = await client.delete(url, follow_redirects=True)

    return submenu


@pytest.fixture
async def non_existent_submenu_response(
        client: AsyncClient,
        get_app: FastAPI,
        get_menu_id: uuid.UUID
) -> Response:
    """Request to get a non-existent submenu."""

    url = get_app.url_path_for(
        'get_detail_submenu',
        menu_id=get_menu_id,
        submenu_id='5372d4ba-1e98-4b37-b1fe-000000000000'
    )
    submenu = await client.get(url, follow_redirects=True)

    return submenu


@pytest.fixture
def response_submenu_data(
        get_submenu_id: uuid.UUID,
        get_menu_id: uuid.UUID
) -> Dict[str, Union[str, int, uuid.UUID]]:
    """Response data of submenu."""

    return {
        'id': get_submenu_id,
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'menu_id': get_menu_id,
        'dishes_count': 0
    }


@pytest.fixture
def create_submenu_data() -> Dict[str, str]:
    """Data for create of submenu."""

    return {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }


@pytest.fixture
def update_submenu_data() -> Dict[str, str]:
    """Data for update of submenu."""

    return {
        'title': 'Updated submenu',
        'description': 'Updated submenu description'
    }
