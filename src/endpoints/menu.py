import uuid
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.db.schemas import Status
from src.db.schemas.menu import (
    MenuCreate,
    MenuResponse,
    MenuUpdate,
)
from src.services.menu import (
    MenuService,
    get_menu_service,
)


menu_route = APIRouter()


@menu_route.get('/menus',
                summary='Get list',
                description='Get list of menus',
                response_model=List[MenuResponse],
                status_code=status.HTTP_200_OK)
async def get_list_menu(menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.get_list()


@menu_route.post('/menus',
                 summary='Create menu',
                 description='Create new menu',
                 response_model=MenuResponse,
                 status_code=status.HTTP_201_CREATED)
async def create_menu(data: MenuCreate,
                      menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.create(data)


@menu_route.get('/menus/{menu_id}',
                summary='get detail',
                description='Get detail of menu by menu_id',
                response_model=MenuResponse,
                status_code=status.HTTP_200_OK)
async def get_detail_menu(menu_id: uuid.UUID,
                          menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.get_detail(menu_id=menu_id)


@menu_route.patch('/menus/{menu_id}',
                  summary='Update menu',
                  description='Update menu by menu_id',
                  response_model=MenuResponse,
                  status_code=status.HTTP_200_OK)
async def update_menu(menu_id: uuid.UUID,
                      data: MenuUpdate,
                      menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.update(menu_id=menu_id, data=data)


@menu_route.delete('/menus/{menu_id}',
                   summary='Delete menu',
                   description='Delete menu by menu_id',
                   response_model=Status,
                   status_code=status.HTTP_200_OK)
async def delete_menu(menu_id: uuid.UUID,
                      menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.delete(menu_id)
