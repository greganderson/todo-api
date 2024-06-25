from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import get_db
from models import Todo
from schemas import CreateTodoResponse


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/todos")
async def get_todos(db: Session = Depends(get_db)) -> list[Todo]:
    return db.exec(select(Todo)).all()


@app.post("/todos")
async def create_todo(todo: Todo, db: Session = Depends(get_db)) -> CreateTodoResponse:
    todo_exists = db.get(Todo, todo.id) is not None
    if not todo_exists:
        db.add(todo)
        db.commit()
        return CreateTodoResponse(success=True, message="TODO successfully created")
    return CreateTodoResponse(success=False, message="Todo already exists")
