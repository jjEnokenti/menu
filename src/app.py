from fastapi import (
    APIRouter,
    FastAPI,
)

from src.endpoints.menu import menu_route


app = FastAPI()

main_route = APIRouter(
    prefix='/api/v1'
)

main_route.include_router(menu_route)
app.include_router(main_route)
