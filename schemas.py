from pydantic import BaseModel

from models import Todo


class Category(BaseModel):
    title: str
    todos: list[Todo]


class CreateTodoResponse(BaseModel):
    success: bool
    message: str
