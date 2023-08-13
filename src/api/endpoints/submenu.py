import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.api.schemas import Status, SubmenuCreate, SubmenuResponse, SubmenuUpdate
from src.api.services.submenu import SubmenuService
from src.dependencies import get_submenu_service

submenu_route = APIRouter()


@submenu_route.get(
    '/submenus',
    summary='Get list',
    description='Get list of submenus',
    response_model=list[SubmenuResponse],
    status_code=status.HTTP_200_OK,
)
async def get_list_submenu(
        menu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.get_list(menu_id=menu_id)


@submenu_route.post(
    '/submenus',
    summary='Create submenu',
    description='Create new submenu',
    response_model=SubmenuResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
        menu_id: uuid.UUID,
        data: SubmenuCreate,
        background_tasks: BackgroundTasks,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.create(
        menu_id=menu_id,
        data=data,
        background_tasks=background_tasks,
    )


@submenu_route.get(
    '/submenus/{submenu_id}',
    summary='get detail',
    description='Get detail of submenu by submenu_id',
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
)
async def get_detail_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.get_detail(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@submenu_route.patch(
    '/submenus/{submenu_id}',
    summary='Update submenu',
    description='Update submenu by submenu_id',
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
)
async def update_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        data: SubmenuUpdate,
        background_tasks: BackgroundTasks,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.update(
        menu_id=menu_id,
        submenu_id=submenu_id,
        data=data,
        background_tasks=background_tasks,
    )


@submenu_route.delete(
    '/submenus/{submenu_id}',
    summary='Delete submenu',
    description='Delete submenu by submenu_id',
    response_model=Status,
    status_code=status.HTTP_200_OK,
)
async def delete_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        background_tasks: BackgroundTasks,
        submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.delete(
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_tasks=background_tasks,
    )
