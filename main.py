from collections import defaultdict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import get_db
from models import Todo
from schemas import Category, CreateTodoResponse


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
async def get_todos(db: Session = Depends(get_db)) -> list[Category]:
    """Returns the todos grouped by category"""

    todos = db.exec(select(Todo)).all()
    categories = defaultdict(list)
    for todo in todos:
        categories[todo.category].append(todo)

    return [
        Category(title=title, todos=category_todos)
        for title, category_todos in categories.items()
    ]


@app.get("/todos/{category}")
async def get_todos_by_category(
    category: str, db: Session = Depends(get_db)
) -> list[str]:
    return map(
        lambda item: item.title,
        db.exec(select(Todo).where(Todo.category == category)).all(),
    )


@app.get("/categories")
async def get_categories(db: Session = Depends(get_db)) -> list[str]:
    return db.exec(select(Todo.category)).all()


@app.post("/todos")
async def create_todo(todo: Todo, db: Session = Depends(get_db)) -> CreateTodoResponse:
    todo_exists = db.get(Todo, todo.id) is not None
    if not todo_exists:
        db.add(todo)
        db.commit()
        return CreateTodoResponse(success=True, message="TODO successfully created")
    raise HTTPException(
        status_code=400, detail=f"Todo with ID {todo.id} already exists"
    )
