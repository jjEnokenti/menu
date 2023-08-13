import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response


@pytest.fixture
async def all_data_response(
        get_app: FastAPI,
        client: AsyncClient
) -> Response:
    """Request to return the list of menus."""

    url = get_app.url_path_for('get_all_detail_data')
    data = await client.get(url, follow_redirects=True)

    return data


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
    menus = menus_list_response.json()

    if menus:
        return menus[-1].get('id')

    return uuid.uuid4()


@pytest.fixture
async def create_menu_response(
        get_app: FastAPI,
        client: AsyncClient,
        create_menu_data: dict[str, str]
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
        update_menu_data: dict[str, str]
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
def response_all_data(
        all_data_response: Response,
) -> list:
    """Response data of menu."""

    return [{
        'id': menu.get('id'),
        'title': menu.get('title'),
        'description': menu.get('description'),
        'submenus': [{
            'id': submenu.get('id'),
            'title': submenu.get('title'),
            'description': submenu.get('description'),
            'dishes': [{
                'id': dish.get('id'),
                'title': dish.get('title'),
                'description': dish.get('description'),
                'price': dish.get('price'),
            } for dish in submenu['dishes']]
        } for submenu in menu['submenus']]
    } for menu in all_data_response.json()]


@pytest.fixture
def response_menu_data(
        get_menu_id: uuid.UUID,
        detail_menu_response: Response
) -> dict[str, str | int | uuid.UUID]:
    """Response data of menu."""

    return {
        'id': get_menu_id,
        'title': detail_menu_response.json().get('title'),
        'description': detail_menu_response.json().get('description'),
        'submenus_count': detail_menu_response.json().get('submenus_count'),
        'dishes_count': detail_menu_response.json().get('dishes_count')
    }


@pytest.fixture
def create_menu_data() -> dict[str, str]:
    """Data for create of menu."""

    return {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }


@pytest.fixture
def update_menu_data() -> dict[str, str]:
    """Data for update of menu."""

    return {
        'title': 'My updated menu',
        'description': 'My updated menu description'
    }
