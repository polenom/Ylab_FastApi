from fastapi import APIRouter, status, HTTPException
from menu.forms import BaseForm, PatchForm
from menu.models import *
from menu.utils.database import MenuSession

router = APIRouter()
conn = MenuSession.get_connect()


@router.get('/menus/{item_id}')
def menu_get(item_id: str):
    result = conn.get_elem(int(item_id))
    if not result:
        raise HTTPException(status_code=404, detail="menu not found")
    return result


@router.get('/menus', status_code=status.HTTP_200_OK)
def menus_get():
    result = conn.get_elems()
    return result

@router.post('/menus', status_code=status.HTTP_201_CREATED)
def menu_post(menu_form: BaseForm):
    result =  conn.create(Menu(**menu_form.dict()))
    if result.id is not None:
        return conn.get_elem(result.id)
    return menu_form.dict()

@router.patch('/menus/{item_id}', status_code=status.HTTP_200_OK)
def menu_patch(item_id: str, patch_form: PatchForm):
    result = conn.update(int(item_id), patch_form.dict(exclude_unset= True))
    if result:
        return result
    return {}



@router.delete('/menus/{item_id}', status_code=status.HTTP_200_OK)
def menu_delete(item_id: str):
    result = conn.delete(int(item_id))
    message = f'''The menu has{"n't" * abs(result - 1)} been deleted'''
    return {
        "status": result,
        "message": message
    }
