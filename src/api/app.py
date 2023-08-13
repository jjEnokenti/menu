from fastapi import APIRouter, FastAPI

from src.api.endpoints import dish_route, menu_route, submenu_route

__all__ = (
    'app',
)

app = FastAPI(
    title='Restaurant menu API',
    description='FastAPI project',
    version='0.1.1',
    docs_url='/api/v1/docs',
)

main_route = APIRouter(
    prefix='/api/v1',
)

main_route.include_router(
    menu_route,
    tags=['menus'],
)
main_route.include_router(
    submenu_route,
    prefix='/menus/{menu_id}',
    tags=['submenus'],
)
main_route.include_router(
    dish_route,
    prefix='/menus/{menu_id}/submenus/{submenu_id}',
    tags=['dishes'],
)
app.include_router(main_route)
