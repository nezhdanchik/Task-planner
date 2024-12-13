import logging

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends
from pydantic import BaseModel

from app.api.schemas.user_schema import UserOut
from app.api.endpoints.account import get_current_user
from app.api.exceptions import UserException
from app.api.schemas.task_schema import TaskCreate, TaskPriority, TaskStatus, \
    TaskUpdate
from app.api.schemas import enums
from app.db.interaction import TaskDAO
from app.redis_interaction import UserTasksCache

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

async def delete_cache(user=Depends(get_current_user)):
    statuses = [st.value for st in enums.TaskStatus]
    for st in statuses:
        cache = UserTasksCache(st, user.id)
        await cache.delete()
    logger.info('cache deleted')
    print('cache was deleted')


async def check_user_has_access_to_task(task_id: int,
                                        user=Depends(get_current_user)):
    task = await TaskDAO.get_one_or_none(task_id)
    if not task or task.user_id != user.id:
        raise UserException(
            detail="No such task", status_code=status.HTTP_400_BAD_REQUEST
        )
    return task


router = APIRouter(
    dependencies=[
        Depends(get_current_user),
    ]
)


@router.post("/", dependencies=[Depends(delete_cache)])
async def create_task(task: TaskCreate,
                      user: Annotated[UserOut, Depends(get_current_user)]):
    new_task = await TaskDAO.create(task, user_id=user.id, exclude_unset=False)
    return new_task


@router.get("/{task_id}/",
            dependencies=[Depends(check_user_has_access_to_task)])
async def get_task(task_id: int):
    task = await TaskDAO.get_one_or_none(task_id)
    return task


@router.post("/{task_id}/end/",
             dependencies=[Depends(delete_cache),
                           Depends(check_user_has_access_to_task)])
async def finish_task(task_id: int):
    class FinishTask(BaseModel):
        finished: datetime

    return await TaskDAO.update(
        task_id, values_to_update=FinishTask(finished=datetime.now())
    )


@router.patch("/{task_id}/",
              dependencies=[Depends(delete_cache),
                            Depends(check_user_has_access_to_task)])
async def update_task(task_id: int, task_for_update: TaskUpdate):
    updated_task = await TaskDAO.update(task_id, task_for_update)
    return updated_task


@router.delete("/{task_id}/",
               dependencies=[Depends(delete_cache),
                             Depends(check_user_has_access_to_task)])
async def delete_task(task_id: int):
    successful = await TaskDAO.delete_task(task_id)
    if not successful:
        return UserException(
            detail="No such task", status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"message": "successful"}


@router.put("/{task_id}/status",
            dependencies=[Depends(delete_cache),
                          Depends(check_user_has_access_to_task)])
async def change_status(task_id: int, status_model: TaskStatus):
    updated_task = await TaskDAO.update(task_id, values_to_update=status_model)
    if not updated_task:
        return UserException(
            detail="No such task", status_code=status.HTTP_400_BAD_REQUEST
        )
    return updated_task


@router.put("/{task_id}/priority",
            dependencies=[Depends(delete_cache),
                          Depends(check_user_has_access_to_task)])
async def change_priority(task_id: int, priority_model: TaskPriority):
    updated_task = await TaskDAO.update(task_id,
                                        values_to_update=priority_model)
    if not updated_task:
        return UserException(
            detail="No such task", status_code=status.HTTP_400_BAD_REQUEST
        )
    return updated_task
