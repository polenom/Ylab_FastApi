from fastapi import APIRouter, status, HTTPException
from menu.forms import BaseForm, PatchForm
from menu.models import *
from menu.utils.database import MenuSession, SubmenuSession

router = APIRouter()
conn = SubmenuSession.get_connect()


@router.get('/{menu_id}/submenus/{submenu_id}')
def submenu_get(menu_id: str, submenu_id: str):
    result = conn.get_elem(int(menu_id), int(submenu_id))
    if not result:
        raise HTTPException(status_code=404, detail="submenu not found")
    return result


@router.get('/{menu_id}/submenus/', status_code=status.HTTP_200_OK)
def submenus_get(menu_id: str):
    result = conn.get_elems(int(menu_id))
    return result


@router.post('/{menu_id}/submenus/', status_code=status.HTTP_201_CREATED)
def submenu_post( menu_id: str,menu_form: BaseForm):
    result =  conn.create(Submenu(**menu_form.dict(),menu_id=int(menu_id)))
    if result.id is not None:
        return conn.get_elem(int(menu_id), result.id)
    return menu_form.dict()

@router.patch('/{menu_id}/submenus/{submenu_id}', status_code=status.HTTP_200_OK)
def submenu_patch(menu_id: str, submenu_id: str, patch_form: PatchForm):
    result = conn.update(int(menu_id), int(submenu_id), patch_form.dict(exclude_unset= True))
    if not result:
        raise HTTPException(status_code=404, detail="submenu not found")
    return result


@router.delete('/{menu_id}/submenus/{submenu_id}', status_code=status.HTTP_200_OK)
def submenu_delete(menu_id: str, submenu_id: str):
    result = conn.delete(int(menu_id), int(submenu_id))
    print(result)
    message = f'''The menu has{"n't" * abs(result - 1)} been deleted'''
    return {
        "status": result,
        "message": message
    }
