import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.api.schemas import DishCreate, DishResponse, DishUpdate, Status
from src.api.services.dish import DishService
from src.dependencies import get_dish_service

dish_route = APIRouter()


@dish_route.get(
    '/dishes',
    summary='Get list',
    description='Get list of dishes',
    response_model=list[DishResponse],
    status_code=status.HTTP_200_OK,
)
async def get_list_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.get_list(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@dish_route.post(
    '/dishes',
    summary='Create dish',
    description='Create new dish',
    response_model=DishResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        data: DishCreate,
        background_tasks: BackgroundTasks,
        dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.create(
        menu_id=menu_id,
        submenu_id=submenu_id,
        data=data,
        background_tasks=background_tasks,
    )


@dish_route.get(
    '/dishes/{dish_id}',
    summary='get detail',
    description='Get detail of dish by dish_id',
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
)
async def get_detail_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.get_detail(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )


@dish_route.patch(
    '/dishes/{dish_id}',
    summary='Update dish',
    description='Update dish by dish_id',
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
)
async def update_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        data: DishUpdate,
        background_tasks: BackgroundTasks,
        dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.update(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        data=data,
        background_tasks=background_tasks,
    )


@dish_route.delete(
    '/dishes/{dish_id}',
    summary='Delete dish',
    description='Delete dish by dish_id',
    response_model=Status,
    status_code=status.HTTP_200_OK,
)
async def delete_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        background_tasks: BackgroundTasks,
        dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.delete(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        background_tasks=background_tasks,
    )
