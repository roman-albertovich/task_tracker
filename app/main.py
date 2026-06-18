from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uuid
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TaskDB, TaskCreate, TaskResponse, TaskStatus

app = FastAPI(title="Task Manager API")

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task_date: TaskCreate, db: Session = Depends(get_db)):
    """Создание новой задачи в PostgreSQL"""
    # Мапим данные из Pydantic-модели в SQLAlchemy-модель БД
    new_task = TaskDB(
        id=uuid.uuid4(),
        name=task_date.name,
        status=TaskStatus.NEW,
        description=task_date.description,
        author=task_date.author
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task) # Подтягиваем сгенерированные данные из БД
    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    """Получение всех задач из базы данных"""
    tasks = db.query(TaskDB).all()
    return tasks

@app.get("/")
def dom_root():
    """Отдаёт главную страницу интерфейса"""
    # Выислеяем абсолютный путь к файле index.html
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(current_dir, "static", "index.html"))