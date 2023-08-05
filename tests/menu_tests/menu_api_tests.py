import uuid

from httpx import Response


class TestMenuAPI:

    async def test_get_menu_empty_list(
            self,
            menus_list_response: Response
    ):
        """Test for getting an empty list of menus."""

        assert (
            menus_list_response.headers.get(
                'content-type') == 'application/json'
        )
        assert menus_list_response.status_code == 200
        assert menus_list_response.json() == []

    async def test_menu_create_successful(
            self,
            create_menu_response: Response,
            response_menu_data: dict[str, str | int | uuid.UUID],
            create_menu_data: dict[str, str]
    ):
        """Test the successful creation of the menu."""

        assert create_menu_response.status_code == 201
        assert isinstance(create_menu_response.json(), dict)
        assert (
            create_menu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert (
            create_menu_response.json().get(
                'id') == response_menu_data.get('id')
        )
        assert (
            create_menu_response.json().get(
                'title') == create_menu_data.get('title')
        )
        assert (
            create_menu_response.json().get(
                'description') == create_menu_data.get('description')
        )
        assert create_menu_response.json() == response_menu_data

    async def test_get_menu_list_not_empty(
            self,
            menus_list_response: Response,
            response_menu_data: dict[str, str | int | uuid.UUID]
    ):
        """Test for getting a list of menus after creation."""

        assert menus_list_response.status_code == 200
        assert len(menus_list_response.json()) == 1
        assert isinstance(menus_list_response.json(), list)
        assert menus_list_response.json() == [response_menu_data]

    async def test_get_menu_detail_successful(
            self,
            detail_menu_response: Response,
            response_menu_data: dict[str, str | int | uuid.UUID],
            create_menu_data: dict[str, str]
    ):
        """Test for getting a detail of menu."""

        assert detail_menu_response.status_code == 200
        assert (
            detail_menu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert isinstance(detail_menu_response.json(), dict)
        assert (
            detail_menu_response.json().get(
                'id') == response_menu_data.get('id')
        )
        assert (
            detail_menu_response.json().get(
                'title') == create_menu_data.get('title')
        )
        assert (
            detail_menu_response.json().get(
                'description') == create_menu_data.get('description')
        )

    async def test_update_detail_of_menu_successful(
            self,
            update_menu_response: Response,
            response_menu_data: dict[str, str | int | uuid.UUID],
            update_menu_data: dict[str, str]
    ):
        """Test for successful updating a detail of menu."""

        assert update_menu_response.status_code == 200
        assert isinstance(update_menu_response.json(), dict)
        assert (
            update_menu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert (
            update_menu_response.json().get(
                'id') == response_menu_data.get('id')
        )
        assert (
            update_menu_response.json().get(
                'title') == update_menu_data.get('title')
        )
        assert (
            update_menu_response.json().get(
                'description') == update_menu_data.get('description')
        )

    async def test_get_menu_detail_after_update(
            self,
            detail_menu_response: Response,
            response_menu_data: dict[str, str | int | uuid.UUID],
            update_menu_data: dict[str, str]
    ):
        """Test to check data after update a details of menu."""

        assert detail_menu_response.status_code == 200
        assert isinstance(detail_menu_response.json(), dict)
        assert (
            detail_menu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert (
            detail_menu_response.json().get(
                'id') == response_menu_data.get('id')
        )
        assert (
            detail_menu_response.json().get(
                'title') == update_menu_data.get('title')
        )
        assert (
            detail_menu_response.json().get(
                'description') == update_menu_data.get('description')
        )

    async def test_delete_menu_successful(
            self,
            delete_menu_response: Response
    ):
        """Test to check the deletion of a menu."""

        assert delete_menu_response.status_code == 200
        assert (
            delete_menu_response.headers.get(
                'content-type') == 'application/json'
        )

    async def test_get_menu_empty_list_after_delete(
            self,
            menus_list_response: Response
    ):
        """Test to check menus after deletion of a menu."""

        await self.test_get_menu_empty_list(menus_list_response)

    async def test_get_non_existent_menu(
            self,
            non_existent_menu_response: Response
    ):
        """Test to check a non-existent menu."""

        assert non_existent_menu_response.json().get('detail') == 'menu not found'
        assert non_existent_menu_response.status_code == 404
