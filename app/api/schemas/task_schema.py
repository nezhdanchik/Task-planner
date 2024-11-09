from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str | None
    completed: bool = False

class TaskInDB(Task):
    id: int

class UpdateTask(BaseModel):
    title: str = None
    description: str | None = None
    completed: bool = False