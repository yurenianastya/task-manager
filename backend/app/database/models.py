from pydantic import BaseModel
from typing import List
from enum import Enum

class StatusEnum(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CreateTask(BaseModel):
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    user_id: int

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    user_id: int

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    name: str

class User(BaseModel):
    id: int
    name: str
    tasks: List[Task]

    class Config:
        orm_mode = True