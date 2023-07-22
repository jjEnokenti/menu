from fastapi import (
    APIRouter,
    FastAPI,
)

from src.endpoints.menu import menu_route
from src.endpoints.submenu import submenu_route


app = FastAPI(
    title='Restaurant menu API',
    description='FastApi project',
    version='0.1.1'
)

main_route = APIRouter(
    prefix='/api/v1'
)

main_route.include_router(
    menu_route,
    prefix='/menus',
    tags=['menus'],
)
main_route.include_router(
    submenu_route,
    prefix='/menus/{menu_id}/submenus',
    tags=['submenu'],
)
app.include_router(main_route)
