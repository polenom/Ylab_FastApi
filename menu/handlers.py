from fastapi import APIRouter, status
from menu.forms import MenuForm, PatchForm
from menu.models import *
from sqlalchemy import insert, select
from core.database import MenuSession

router = APIRouter()
conn = MenuSession.get_connect()


@router.post('/menus', name='')
def menu_post(menu_form: MenuForm):
    result =  conn.create(Menu(**menu_form.dict()))
    if result.id is not None:
        return conn.get_elem(result.id)
    return menu_form.dict()

@router.patch('/menus/{item_id}', status_code=status.HTTP_201_CREATED)
def patch_post(item_id: str, patch_form: PatchForm):
    result = conn.update(int(item_id), patch_form.dict(exclude_unset= True))
    print(result)
    if result:
        return result
    return {}


@router.get('/menus/{item_id}', status_code=status.HTTP_200_OK)
def menus_get(item_id: str):
    result = conn.get_elem(int(item_id))
    return result


@router.get('/menus', status_code=status.HTTP_200_OK)
def menu_get():
    result = conn.get_elems()
    return result


@router.delete('/menus/{item_id}', status_code=status.HTTP_200_OK)
def menu_delete(item_id: str):
    result = conn.delete(int(item_id))
    message = f'''The menu has{"n't" * abs(result - 1)} been deleted'''
    return {
        "status": result,
        "message": message
    }
