from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID
from pydantic import BaseModel

class Error(BaseModel):
    detail: str | None = None


class Priority(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Status(StrEnum):
    PENDING = auto()
    PROGRESS = auto()
    COMPLETED = auto()


class CreateTaskSchema(BaseModel):
    priority: Priority | None  = Priority.LOW
    status: Status | None  = Status.PENDING
    task: str


class GetTaskSchema(CreateTaskSchema):
    id: UUID | None
    created: datetime


class ListTasksSchema(BaseModel):
    tasks: list[GetTaskSchema]
