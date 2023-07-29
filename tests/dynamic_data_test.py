import uuid
from typing import (
    Dict,
    Union,
)

import pytest
from httpx import Response


class TestDynamicData:
    """A tests for checking dynamic data."""

    async def test_menu_create(
            self,
            create_menu_response: Response,
            response_menu_data: Dict[str, Union[str, int, uuid.UUID]]
    ):
        """Test creating a menu for further testing of the dynamic data."""

        assert create_menu_response.status_code == 201
        assert isinstance(create_menu_response.json(), dict)
        assert (
                create_menu_response.headers.get('content-type') ==
                'application/json'
        )
        assert (
                create_menu_response.json().get('id') ==
                response_menu_data.get('id')
        )
        assert create_menu_response.json().get('submenus_count') == 0
        assert create_menu_response.json().get('dishes_count') == 0

    async def test_submenu_create(
            self,
            create_submenu_response: Response,
            response_submenu_data: Dict[str, Union[str, int, uuid.UUID]]
    ):
        """Test creating a submenu for further testing of the dynamic data."""

        assert create_submenu_response.status_code == 201
        assert isinstance(create_submenu_response.json(), dict)
        assert (
                create_submenu_response.headers.get('content-type') ==
                'application/json'
        )
        assert (
                create_submenu_response.json().get('id') ==
                response_submenu_data.get('id')
        )
        assert create_submenu_response.json().get('dishes_count') == 0

    @pytest.mark.parametrize(
        'create_dish_response', [
            'create_dish_data',
            'create_dish_data_second'
        ],
        indirect=['create_dish_response']
    )
    async def test_dish_create_successful(
            self,
            create_dish_response: Response,
            response_dish_data: Dict[str, Union[str, int, uuid.UUID]]
    ):
        """Test the successful creation of dish."""

        assert create_dish_response.status_code == 201
        assert isinstance(create_dish_response.json(), dict)
        assert (
                create_dish_response.headers.get('content-type') ==
                'application/json'
        )
        assert (
                create_dish_response.json().get('id') ==
                response_dish_data.get('id')
        )
        assert (
                create_dish_response.json().get('title') ==
                response_dish_data.get('title')
        )
        assert (
                create_dish_response.json().get('description') ==
                response_dish_data.get('description')
        )

    async def test_get_detail_menu_with_dynamic_data(
            self,
            detail_menu_response: Response,
            get_menu_id: uuid.UUID
    ):
        """Test for getting a detail of menus after 2 dish and 1 submenu creation."""

        assert detail_menu_response.status_code == 200
        assert (
                detail_menu_response.headers.get('content-type') ==
                'application/json'
        )
        assert isinstance(detail_menu_response.json(), dict)
        assert (
                detail_menu_response.json().get('id') ==
                get_menu_id
        )
        assert detail_menu_response.json().get('submenus_count') == 1
        assert detail_menu_response.json().get('dishes_count') == 2

    async def test_get_submenu_detail_with_dynamic_data(
            self,
            detail_submenu_response: Response,
            get_submenu_id: uuid.UUID
    ):
        """Test for getting a detail of submenu after 2 dish creation."""

        assert detail_submenu_response.status_code == 200
        assert (
                detail_submenu_response.headers.get('content-type') ==
                'application/json'
        )
        assert isinstance(detail_submenu_response.json(), dict)
        assert (
                detail_submenu_response.json().get('id') ==
                get_submenu_id
        )
        assert detail_submenu_response.json().get('dishes_count') == 2

    async def test_delete_submenu_for_check_dynamic_data(
            self,
            delete_submenu_response: Response
    ):
        """Test to check the deletion of a submenu for dynamic data tests."""

        assert delete_submenu_response.status_code == 200
        assert (
                delete_submenu_response.headers.get('content-type') ==
                'application/json'
        )

    async def test_get_submenu_empty_list_after_delete(
            self,
            submenus_list_response: Response
    ):
        """Test for getting an empty list of submenus after deletion for dynamic data tests."""

        assert (
                submenus_list_response.headers.get('content-type') ==
                'application/json'
        )
        assert submenus_list_response.status_code == 200
        assert submenus_list_response.json() == []

    async def test_get_list_of_dishes_empty_after_delete_submenu(
            self,
            dish_list_response: Response
    ):
        """Test for getting an empty list of dishes after delete submenu."""

        assert (
                dish_list_response.headers.get('content-type') ==
                'application/json'
        )
        assert dish_list_response.status_code == 200
        assert dish_list_response.json() == []

    async def test_get_menu_detail_for_check_dynamic_data(
            self,
            detail_menu_response: Response,
            response_menu_data: Dict[str, Union[str, int, uuid.UUID]]
    ):
        """Test for getting a detail of menu for check dynamic data."""

        assert detail_menu_response.status_code == 200
        assert (
                detail_menu_response.headers.get('content-type') ==
                'application/json'
        )
        assert isinstance(detail_menu_response.json(), dict)
        assert (
                detail_menu_response.json().get('id') ==
                response_menu_data.get('id')
        )
        assert detail_menu_response.json().get('submenus_count') == 0
        assert detail_menu_response.json().get('dishes_count') == 0

    async def test_delete_of_menu_success_for_dynamic_data_tests(
            self,
            delete_menu_response: Response
    ):
        """Test to delete of menu for dynamic data tests."""

        assert delete_menu_response.status_code == 200
        assert (
                delete_menu_response.headers.get('content-type') ==
                'application/json'
        )

    async def test_get_menu_empty_list_after_deletion_for_dynamic_data_tests(
            self,
            menus_list_response: Response
    ):
        """Test to check of menu after deletion for dynamic datatests."""

        assert (
                menus_list_response.headers.get('content-type') ==
                'application/json'
        )
        assert menus_list_response.status_code == 200
        assert menus_list_response.json() == []
