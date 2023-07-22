import uuid
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.db.schemas import Status
from src.db.schemas.submenu import (
    SubmenuCreate,
    SubmenuResponse,
    SubmenuUpdate,
)
from src.services.submenu import (
    SubmenuService,
    get_submenu_service,
)


submenu_route = APIRouter()


@submenu_route.get('/submenus',
                   summary='Get list',
                   description='Get list of submenus',
                   response_model=List[SubmenuResponse],
                   status_code=status.HTTP_200_OK)
async def get_list_submenu(menu_id: uuid.UUID,
                           submenu_service: SubmenuService = Depends(get_submenu_service)):
    return await submenu_service.get_list(menu_id)


@submenu_route.post('/submenus',
                    summary='Create submenu',
                    description='Create new submenu',
                    response_model=SubmenuResponse,
                    status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: uuid.UUID,
                         data: SubmenuCreate,
                         submenu_service: SubmenuService = Depends(get_submenu_service)):
    return await submenu_service.create(menu_id=menu_id, data=data)


@submenu_route.get('/submenus/{submenu_id}',
                   summary='get detail',
                   description='Get detail of submenu by submenu_id',
                   response_model=SubmenuResponse,
                   status_code=status.HTTP_200_OK)
async def get_detail_submenu(submenu_id: uuid.UUID,
                             submenu_service: SubmenuService = Depends(get_submenu_service)):
    return await submenu_service.get_detail(submenu_id=submenu_id)


@submenu_route.patch('/submenus/{submenu_id}',
                     summary='Update submenu',
                     description='Update submenu by submenu_id',
                     response_model=SubmenuResponse,
                     status_code=status.HTTP_200_OK)
async def update_submenu(submenu_id: uuid.UUID,
                         data: SubmenuUpdate,
                         submenu_service: SubmenuService = Depends(get_submenu_service)):
    return await submenu_service.update(submenu_id=submenu_id, data=data)


@submenu_route.delete('/submenus/{submenu_id}',
                      summary='Delete submenu',
                      description='Delete submenu by submenu_id',
                      response_model=Status,
                      status_code=status.HTTP_200_OK)
async def delete_submenu(submenu_id: uuid.UUID,
                         submenu_service: SubmenuService = Depends(get_submenu_service)):
    return await submenu_service.delete(submenu_id)
