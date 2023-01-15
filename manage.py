from fastapi import FastAPI
from menu.handlers import router as router_menu


def get_service():
    service = FastAPI()
    service.include_router(router_menu, prefix='/api/v1')
    return service


app = get_service()

