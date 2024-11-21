from pydantic import BaseModel, Field
from schemas import enums


class TaskStatus(BaseModel):
    status: enums.TaskStatus

class TaskPriority(BaseModel):
    priority: enums.TaskPriority

class TaskStatusPriority(TaskStatus, TaskPriority):
    pass

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(min_length=1, max_length=2000, default=None)
    status: enums.TaskStatus = enums.TaskStatus.CREATED.value
    priority: enums.TaskPriority = enums.TaskPriority.LOW.value

    model_config = {"use_enum_values": True}

    # @field_validator('deadline')
    # @classmethod
    # def check_deadline(cls, v: datetime):
    #     if v.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
    #         print('error!!! deadline must be in the future')
    #         raise TaskException('deadline must be in the future')
    #     return v.replace(tzinfo=None)


class TaskUpdate(BaseModel):
    title: str | None = Field(min_length=1, max_length=20)
    description: str | None = Field(min_length=1, max_length=200, default=None)
    status: enums.TaskStatus | None = enums.TaskStatus.CREATED.value
    priority: enums.TaskPriority | None = enums.TaskPriority.LOW.value

    model_config = {"use_enum_values": True}
