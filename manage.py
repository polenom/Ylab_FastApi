from fastapi import FastAPI
from menu.routers.menu import router as router_menu
from menu.routers.submenu import router as router_submenu
from menu.routers.dish import router as router_dish


def get_service():
    service = FastAPI()
    service.include_router(router_dish, prefix='/api/v1/menus')
    service.include_router(router_submenu, prefix='/api/v1/menus')
    service.include_router(router_menu, prefix='/api/v1')
    return service


app = get_service()

