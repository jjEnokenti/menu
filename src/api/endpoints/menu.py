import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.api.schemas import MenuCreate, MenuInDB, MenuResponse, MenuUpdate, Status
from src.api.services.menu import MenuService
from src.dependencies import get_menu_service

menu_route = APIRouter()


@menu_route.get(
    '/get_all',
    status_code=status.HTTP_200_OK,
    response_model=list[MenuInDB]
)
async def get_all_detail_data(service: MenuService = Depends(get_menu_service)):
    return await service.get_all_detail_data()


@menu_route.get(
    '/menus',
    summary='Get only list of menus',
    description='Get list of menus',
    response_model=list[MenuResponse],
    status_code=status.HTTP_200_OK,
)
async def get_list_menu(menu_service: MenuService = Depends(get_menu_service)):
    return await menu_service.get_list()


@menu_route.post(
    '/menus',
    summary='Create menu',
    description='Create new menu',
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
        data: MenuCreate,
        background_tasks: BackgroundTasks,
        menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.create(
        data=data,
        background_tasks=background_tasks,
    )


@menu_route.get(
    '/menus/{menu_id}',
    summary='get detail a menu',
    description='Get detail of menu by menu_id',
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
)
async def get_detail_menu(
        menu_id: uuid.UUID,
        menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.get_detail(menu_id=menu_id)


@menu_route.patch(
    '/menus/{menu_id}',
    summary='Update menu',
    description='Update menu by menu_id',
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
)
async def update_menu(
        menu_id: uuid.UUID,
        data: MenuUpdate,
        background_tasks: BackgroundTasks,
        menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.update(
        menu_id=menu_id,
        data=data,
        background_tasks=background_tasks,
    )


@menu_route.delete(
    '/menus/{menu_id}',
    summary='Delete menu',
    description='Delete menu by menu_id',
    response_model=Status,
    status_code=status.HTTP_200_OK,
)
async def delete_menu(
        menu_id: uuid.UUID,
        background_tasks: BackgroundTasks,
        menu_service: MenuService = Depends(get_menu_service),
):
    return await menu_service.delete(
        menu_id=menu_id,
        background_tasks=background_tasks,
    )
