import uuid

from httpx import Response


class TestSubmenuAPI:

    async def test_menu_create_for_submenu_tests(
            self,
            create_menu_response: Response,
            response_menu_data: dict[str, str | int | uuid.UUID],
            create_menu_data: dict[str, str]
    ):
        """Test creating a menu for further testing of the submenu."""

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

    async def test_get_submenu_empty_list(
            self,
            submenus_list_response: Response
    ):
        """Test for getting an empty list of submenus."""

        assert (
            submenus_list_response.headers.get(
                'content-type') == 'application/json'
        )
        assert submenus_list_response.status_code == 200
        assert submenus_list_response.json() == []

    async def test_submenu_create_successful(
            self,
            create_submenu_response: Response,
            response_submenu_data: dict[str, str | int | uuid.UUID],
            create_submenu_data: dict[str, str]
    ):
        """Test the successful creation of the submenu."""

        assert create_submenu_response.status_code == 201
        assert isinstance(create_submenu_response.json(), dict)
        assert (
            create_submenu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert (
            create_submenu_response.json().get(
                'id') == response_submenu_data.get('id')
        )
        assert (
            create_submenu_response.json().get(
                'title') == create_submenu_data.get('title')
        )
        assert (
            create_submenu_response.json().get(
                'description') == create_submenu_data.get('description')
        )

    async def test_get_submenu_list_not_empty(
            self,
            submenus_list_response: Response,
            response_submenu_data: dict[str, str | int | uuid.UUID]
    ):
        """Test for getting a list of submenus after creation."""

        assert submenus_list_response.status_code == 200
        assert len(submenus_list_response.json()) == 1
        assert isinstance(submenus_list_response.json(), list)
        assert submenus_list_response.json() == [response_submenu_data]

    async def test_get_submenu_detail_successful(
            self,
            detail_submenu_response: Response,
            response_submenu_data: dict[str, str | int | uuid.UUID],
            create_submenu_data: dict[str, str]
    ):
        """Test for getting a detail of submenu."""

        assert detail_submenu_response.status_code == 200
        assert (
            detail_submenu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert isinstance(detail_submenu_response.json(), dict)
        assert (
            detail_submenu_response.json().get(
                'id') == response_submenu_data.get('id')
        )
        assert (
            detail_submenu_response.json().get(
                'title') == create_submenu_data.get('title')
        )
        assert (
            detail_submenu_response.json().get(
                'description') == create_submenu_data.get('description')
        )
        assert (
            detail_submenu_response.json().get(
                'menu_id') == response_submenu_data.get('menu_id')
        )

    async def test_update_detail_of_submenu_successful(
            self,
            update_submenu_response: Response,
            response_submenu_data: dict[str, str | int | uuid.UUID],
            update_submenu_data: dict[str, str]
    ):
        """Test for successful updating a detail of submenu."""

        assert update_submenu_response.status_code == 200
        assert isinstance(update_submenu_response.json(), dict)
        assert (
            update_submenu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert (
            update_submenu_response.json().get(
                'id') == response_submenu_data.get('id')
        )
        assert (
            update_submenu_response.json().get(
                'title') == update_submenu_data.get('title')
        )
        assert (
            update_submenu_response.json().get(
                'description') == update_submenu_data.get('description')
        )
        assert (
            update_submenu_response.json().get(
                'menu_id') == response_submenu_data.get('menu_id')
        )

    async def test_get_submenu_detail_after_updating(
            self,
            detail_submenu_response: Response,
            response_submenu_data: dict[str, str | int | uuid.UUID],
            update_submenu_data: dict[str, str]
    ):
        """Test to check data after update a details of submenu."""

        assert detail_submenu_response.status_code == 200
        assert isinstance(detail_submenu_response.json(), dict)
        assert (
            detail_submenu_response.headers.get(
                'content-type') == 'application/json'
        )
        assert (
            detail_submenu_response.json().get(
                'id') == response_submenu_data.get('id')
        )
        assert (
            detail_submenu_response.json().get(
                'menu_id') == response_submenu_data.get('menu_id')
        )
        assert (
            detail_submenu_response.json().get(
                'title') == update_submenu_data.get('title')
        )
        assert (
            detail_submenu_response.json().get(
                'description') == update_submenu_data.get('description')
        )

    async def test_delete_submenu_successful(
            self,
            delete_submenu_response: Response
    ):
        """Test to check the deletion of a submenu."""

        assert delete_submenu_response.status_code == 200
        assert (
            delete_submenu_response.headers.get(
                'content-type') == 'application/json'
        )

    async def test_get_submenu_empty_list_after_delete(
            self,
            submenus_list_response: Response
    ):
        """Test to check submenus after deletion of a submenu."""

        await self.test_get_submenu_empty_list(submenus_list_response)

    async def test_get_non_existent_submenu(
            self,
            non_existent_submenu_response: Response
    ):
        """Test to check a non-existent submenu."""

        assert non_existent_submenu_response.json().get('detail') == 'submenu not found'
        assert non_existent_submenu_response.status_code == 404

    async def test_delete_of_menu_success(
            self,
            delete_menu_response: Response
    ):
        """Test to delete of menu."""

        assert delete_menu_response.status_code == 200
        assert (
            delete_menu_response.headers.get(
                'content-type') == 'application/json'
        )

    async def test_get_menu_empty_list(
            self,
            menus_list_response: Response
    ):
        """Test to check of menu after deletion."""

        assert (
            menus_list_response.headers.get(
                'content-type') == 'application/json'
        )
        assert menus_list_response.status_code == 200
        assert menus_list_response.json() == []
