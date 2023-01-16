from fastapi import APIRouter, status, HTTPException
from menu.forms import DishForm, PatchDishForm
from menu.models import *
from menu.utils.database import DishSession, SubmenuSession

router = APIRouter()
conn = DishSession.get_connect()


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def dish_get(menu_id: str, submenu_id: str, dish_id: str):
    result = conn.get_elem(int(menu_id), int(submenu_id), int(dish_id))
    if not result:
        raise HTTPException(status_code=404, detail="dish not found")
    return result


@router.get('/{menu_id}/submenus/{submenu_id}/dishes', status_code=status.HTTP_200_OK)
def dishs_get(menu_id: str, submenu_id: str):
    result = conn.get_elems(int(menu_id), int(submenu_id))
    return result


@router.post('/{menu_id}/submenus/{submenu_id}/dishes', status_code=status.HTTP_201_CREATED)
def dish_post(menu_id: str, submenu_id: str, dish_form: DishForm):
    dish_values = dish_form.dict()
    dish_values['price'] = float(dish_values['price'])
    result = conn.create(Dish(**dish_values, submenu_id=int(submenu_id)))
    if result.id is not None:
        return conn.get_elem(int(menu_id), int(submenu_id), result.id)
    return dish_form.dict()


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK)
def dish_patch(menu_id: str, submenu_id: str, dish_id: str, patch_form: PatchDishForm):
    dish_values = patch_form.dict(exclude_unset=True)
    if dish_values.get('price'):
        dish_values['price'] = float(dish_values['price'])
    result = conn.update(int(menu_id), int(submenu_id), int(dish_id), patch_form.dict(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="submenu not found")
    return result


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK)
def dish_delete(menu_id: str, submenu_id: str, dish_id: str):
    result = conn.delete(int(menu_id), int(submenu_id), int(dish_id))
    message = f'''The menu has{"n't" * abs(result - 1)} been deleted'''
    return {
        "status": result,
        "message": message
    }
