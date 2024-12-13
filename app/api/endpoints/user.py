from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.api.endpoints.account import current_user_annotation
from app.api.schemas.task_schema import TaskStatus, TaskInDB
from app.db.interaction import TaskDAO
from app.redis_interaction import UserTasksCache
from app.api.schemas import enums

router = APIRouter()


class TaskResponse(BaseModel):
    tasks: list[dict]


@router.get("/tasks/", response_model=TaskResponse)
async def get_tasks(user: current_user_annotation, status: enums.TaskStatus):
    # проверка в redis
    cache = UserTasksCache(status.value, user.id)
    result = await cache.hget()
    if result:
        return result

    tasks = await TaskDAO.get_all_tasks_with_status(user_id=user.id,
                                                    status=status)
    tasks_models = [TaskInDB.model_validate(task, from_attributes=True) for task
                    in tasks]
    tasks_json = [task.model_dump(mode='json') for task in tasks_models]
    returning = {"tasks": tasks_json}

    # запись в redis
    await cache.hset(returning, time=3600, change_none_in_value=True)

    return returning
