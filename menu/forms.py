from pydantic import BaseModel

class BaseForm(BaseModel):
    title: str
    description: str

class PatchForm(BaseForm):
    title: str = None
    description: str = None


class DishForm(BaseForm):
    price: str


class PatchDishForm(PatchForm):
    price: str = None
