from pydantic import BaseModel


class CreateTodoResponse(BaseModel):
    success: bool
    message: str
