from fastapi import FastAPI
from httpx import AsyncClient


class TestMenuAPI:

    async def get_url(self, name, app, **kwargs):
        return app.url_path_for(
            name,
            **kwargs
        )

    async def detail_menu_url(self, client, app, name):
        menus_url = await self.get_url('get_list_menu', app=app)
        menus = await client.get(menus_url, follow_redirects=True)

        menu_id = menus.json()[0].get('id')

        return await self.get_url(
            name,
            app=app,
            menu_id=menu_id
        )

    async def test_get_menu_empty_list(
            self,
            client: AsyncClient,
            get_app: FastAPI
    ):
        url = await self.get_url(
            name='get_list_menu',
            app=get_app
        )

        response = await client.get(url, follow_redirects=True)

        assert response.status_code == 200
        assert response.json() == []

    async def test_menu_create(
            self,
            client: AsyncClient,
            get_app: FastAPI,
            create_menu_data: dict
    ):
        url = await self.get_url(
            app=get_app,
            name='create_menu'
        )

        response = await client.post(
            url=url,
            json=create_menu_data,
            follow_redirects=True
        )

        assert response.status_code == 201
        assert response.headers.get('content-type') == 'application/json'
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get('id'), str)
        assert response.json().get('title') == 'Menu 1'
        assert response.json().get('description') == 'Menu description 1'

    async def test_get_menu_list_not_empty(
            self,
            client: AsyncClient,
            get_app: FastAPI,
    ):
        url = await self.get_url(
            app=get_app,
            name='get_list_menu'
        )

        response = await client.get(url, follow_redirects=True)

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert isinstance(response.json(), list)

    async def test_get_menu_detail(
            self,
            client: AsyncClient,
            get_app: FastAPI
    ):
        url = await self.detail_menu_url(
            name='get_detail_menu',
            client=client,
            app=get_app
        )

        response = await client.get(url, follow_redirects=True)

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        assert len(response.json()) > 0
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get('id'), str)
        assert response.json().get('title') == 'Menu 1'
        assert response.json().get('description') == 'Menu description 1'

    async def test_update_menu_by_id(
            self,
            client: AsyncClient,
            get_app: FastAPI,
            update_menu_data: dict
    ):
        url = await self.detail_menu_url(
            name='update_menu',
            client=client,
            app=get_app
        )

        response = await client.patch(
            url,
            json=update_menu_data,
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        assert len(response.json()) > 0
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get('id'), str)
        assert response.json().get('title') == 'Updated menu'
        assert response.json().get('description') == 'Updated menu description'

    async def test_delete_menu(
            self,
            client: AsyncClient,
            get_app: FastAPI
    ):
        url = await self.detail_menu_url(
            name='delete_menu',
            client=client,
            app=get_app,
        )

        response = await client.delete(
            url,
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'

    async def test_get_menu_by_id_empty(
            self,
            client: AsyncClient,
            get_app: FastAPI
    ):
        url = await self.get_url(
            'get_detail_menu',
            app=get_app,
            menu_id='5372d4ba-1e98-4b37-b1fe-000000000000'
        )

        response = await client.get(
            url,
            follow_redirects=True
        )

        assert response.json().get('detail') == 'menu not found'
        assert response.status_code == 404
