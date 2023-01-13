from fastapi import APIRouter
from menu.forms import MenuForm

router = APIRouter()


@router.post('/', name='')
def menu_post(menu_form: MenuForm):
    return menu_form.dict()

@router.get('/', name='')
def menu_get():
    return {
        'status': 'OK'
    }