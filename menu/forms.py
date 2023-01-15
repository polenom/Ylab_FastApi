from pydantic import BaseModel

from menu.models import Menu


class MenuForm(BaseModel):
    title: str
    description: str


class PatchForm(BaseModel):
    title: str = None
    description: str = None