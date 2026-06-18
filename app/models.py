from datetime import datetime, timezone
from enum import Enum
import uuid
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

# Базовый класс SQLAlchemy для моделей БД
Base = declarative_base()

# 1. Варианты статусов задачи
class TaskStatus(str, Enum):
    NEW= "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELED = "CANCELED"

# 2. Мрдель SQLAlchemy (описание табицы в PosgreSQL)
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.NEW)
    description = Column(String(540), nullable=True)
    author = Column(String(100), nullable=False) # добавить ForeignKey("users.id") ???
    date_created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    date_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

# 3. Схемы Pydantic (Валидация входящих/исходящих данных API)
class TaskCreate(BaseModel):
    """Схема для создания задачи (то, что присылает клиент)"""
    name: str = Field(..., min_length=1, max_length=100, description="Название задачи")
    description: str | None = Field(None, max_length=540, description="Описание задачи")
    author: str = Field(..., min_length=1, max_length=100, description="Автор задачи")

class TaskUpdate(BaseModel):
    """Схема для обновления задачи (то, что присылает клиент)"""
    id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=100, description="Название задачи")
    status: TaskStatus
    description: str | None = Field(None, max_length=540, description="Описание задачи")
    author: str = Field(..., min_length=1, max_length=100, description="Автор задачи")
    date_created: datetime
    date_updated: datetime

class TaskResponse(BaseModel):
    """Схема ответа API (то, что возвращается клиенту)"""
    id: uuid.UUID
    name: str
    status: TaskStatus
    description: str | None
    author: str
    date_created: datetime
    date_updated: datetime

    """Позволяет Pydantic автоматически читать данных из объектов SQLAlchemy"""

    model_config = ConfigDict(from_attributes=True)