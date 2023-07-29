import uuid
from typing import (
    Dict,
    Union,
)

import pytest
from httpx import Response


class TestDishAPI:
    """Dish API tests."""

    async def test_menu_create_for_dish_tests(
            self,
            create_menu_response: Response,
            response_menu_data: Dict[str, Union[str, int, uuid.UUID]],
    ):
        """Test creating a menu for further testing of the dish."""

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

    async def test_submenu_create_for_dish_tests(
            self,
            create_submenu_response: Response,
            response_submenu_data: Dict[str, Union[str, int, uuid.UUID]],
    ):
        """Test creating a submenu for further testing of the dish."""

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

    async def test_get_list_of_dishes_empty(
            self,
            dish_list_response: Response
    ):
        """Test for getting an empty list of dishes."""

        assert (
                dish_list_response.headers.get('content-type') ==
                'application/json'
        )
        assert dish_list_response.status_code == 200
        assert dish_list_response.json() == []

    @pytest.mark.parametrize(
        'create_dish_response', [
            'create_dish_data'
        ],
        indirect=['create_dish_response']
    )
    async def test_dish_create_successful(
            self,
            create_dish_response: Response,
            response_dish_data: Dict[str, Union[str, int, uuid.UUID]],
    ):
        """Test the successful creation of the dish."""

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

    async def test_get_list_of_dishes_not_empty(
            self,
            dish_list_response: Response,
            response_dish_data: Dict[str, Union[str, int, uuid.UUID]]
    ):
        """Test for getting a list of dishes after creation."""

        assert dish_list_response.status_code == 200
        assert len(dish_list_response.json()) == 1
        assert isinstance(dish_list_response.json(), list)
        assert dish_list_response.json() == [response_dish_data]

    async def test_get_detail_of_dish_successful(
            self,
            detail_dish_response: Response,
            response_dish_data: Dict[str, Union[str, int, uuid.UUID]],
    ):
        """Test for getting a detail of dish."""

        assert detail_dish_response.status_code == 200
        assert (
                detail_dish_response.headers.get('content-type') ==
                'application/json'
        )
        assert isinstance(detail_dish_response.json(), dict)
        assert (
                detail_dish_response.json().get('id') ==
                response_dish_data.get('id')
        )
        assert (
                detail_dish_response.json().get('title') ==
                response_dish_data.get('title')
        )
        assert (
                detail_dish_response.json().get('description') ==
                response_dish_data.get('description')
        )
        assert (
                detail_dish_response.json().get('price') ==
                response_dish_data.get('price')
        )

    async def test_update_detail_of_dish_successful(
            self,
            update_dish_response: Response,
            response_dish_data: Dict[str, Union[str, int, uuid.UUID]],
            update_dish_data: Dict[str, str]
    ):
        """Test for successful updating a detail of dish."""

        assert update_dish_response.status_code == 200
        assert isinstance(update_dish_response.json(), dict)
        assert (
                update_dish_response.headers.get('content-type') ==
                'application/json'
        )
        assert (
                update_dish_response.json().get('id') ==
                response_dish_data.get('id')
        )
        assert (
                update_dish_response.json().get('title') ==
                update_dish_data.get('title')
        )
        assert (
                update_dish_response.json().get('description') ==
                update_dish_data.get('description')
        )
        assert (
                update_dish_response.json().get('price') ==
                update_dish_data.get('price')
        )

    async def test_get_detail_of_dish_after_updating(
            self,
            detail_dish_response: Response,
            response_dish_data: Dict[str, Union[str, int, uuid.UUID]],
            update_dish_data: Dict[str, str]
    ):
        """Test to check data after update a details of dish."""

        assert detail_dish_response.status_code == 200
        assert isinstance(detail_dish_response.json(), dict)
        assert (
                detail_dish_response.headers.get('content-type') ==
                'application/json'
        )
        assert (
                detail_dish_response.json().get('id') ==
                response_dish_data.get('id')
        )
        assert (
                detail_dish_response.json().get('price') ==
                update_dish_data.get('price')
        )
        assert (
                detail_dish_response.json().get('title') ==
                update_dish_data.get('title')
        )
        assert (
                detail_dish_response.json().get('description') ==
                update_dish_data.get('description')
        )

    async def test_delete_dish_successful(
            self,
            delete_dish_response: Response
    ):
        """Test to check the deletion of a dish."""

        assert delete_dish_response.status_code == 200
        assert (
                delete_dish_response.headers.get('content-type') ==
                'application/json'
        )

    async def test_get_list_of_dishes_after_deletion_empty(
            self,
            dish_list_response: Response
    ):
        """Test for getting an empty list of dishes after deletion."""

        await self.test_get_list_of_dishes_empty(dish_list_response)

    async def test_get_non_existent_dish(
            self,
            non_existent_dish_response: Response
    ):
        """Test to check a non-existent dish."""

        assert non_existent_dish_response.json().get('detail') == 'dish not found'
        assert non_existent_dish_response.status_code == 404

    async def test_delete_submenu_successful_for_dish_tests(
            self,
            delete_submenu_response: Response
    ):
        """Test to check the deletion of a submenu for dish tests."""

        assert delete_submenu_response.status_code == 200
        assert (
                delete_submenu_response.headers.get('content-type') ==
                'application/json'
        )

    async def test_get_submenu_empty_list_after_delete(
            self,
            submenus_list_response: Response
    ):
        """Test for getting an empty list of submenus after deletion for dish tests."""

        assert (
                submenus_list_response.headers.get('content-type') ==
                'application/json'
        )
        assert submenus_list_response.status_code == 200
        assert submenus_list_response.json() == []

    async def test_delete_of_menu_success_for_dish_tests(
            self,
            delete_menu_response: Response
    ):
        """Test to delete of menu for dish tests."""

        assert delete_menu_response.status_code == 200
        assert (
                delete_menu_response.headers.get('content-type') ==
                'application/json'
        )

    async def test_get_menu_empty_list_after_deletion_for_dish_tests(
            self,
            menus_list_response: Response
    ):
        """Test to check of menu after deletion for dish tests."""

        assert (
                menus_list_response.headers.get('content-type') ==
                'application/json'
        )
        assert menus_list_response.status_code == 200
        assert menus_list_response.json() == []
