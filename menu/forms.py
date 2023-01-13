from pydantic import BaseModel


class MenuForm(BaseModel):
    title: str
    description: str