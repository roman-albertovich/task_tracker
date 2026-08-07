from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TaskDB, TaskCreate, TaskResponse, TaskStatus, TaskUpdate

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

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: uuid.UUID, db: Session = Depends(get_db)):
    """Получение задачи по id"""
    task = db.query(TaskDB).filter(TaskDB.id == task_id).one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task_by_id(task_id: uuid.UUID, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """Обновление задачи по id"""
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_update = task_data.model_dump(exclude_unset=True)

    for key, value in task_update.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/")
def dom_root():
    """Отдаёт главную страницу интерфейса"""
    # Выислеяем абсолютный путь к файле index.html
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(current_dir, "static", "index.html"))

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_by_id(task_id: uuid.UUID, db: Session = Depends(get_db)):
    """Удаление задачи по id"""
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return None