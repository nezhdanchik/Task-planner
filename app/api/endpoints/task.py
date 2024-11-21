from datetime import datetime

from pydantic import BaseModel

from db.interaction import TaskDAO
from endpoints.account import current_user_annotation
from fastapi import APIRouter, status
from schemas.task_schema import TaskCreate, TaskStatus, TaskPriority, TaskUpdate

from api.exceptions import UserException

router = APIRouter()


@router.post("/")
async def create_task(task: TaskCreate, user: current_user_annotation):
    new_task = await TaskDAO.create(task, user_id=user.id)
    return new_task


@router.get("/{task_id}/")
async def get_task(task_id: int, user: current_user_annotation):
    task = await TaskDAO.get_one_or_none(task_id)
    return task

@router.post("/{task_id}/end/")
async def finish_task(task_id: int, user: current_user_annotation):
    class FinishTask(BaseModel):
        finished: datetime
    return await TaskDAO.update(task_id, values_to_update=FinishTask(finished=datetime.now()))


@router.patch("/{task_id}/")
async def update_task(
    task_id: int, task_for_update: TaskUpdate, user: current_user_annotation
):
    updated_task = await TaskDAO.update(task_id, task_for_update)
    return updated_task


@router.delete("/{task_id}/")
async def delete_task(task_id: int, user: current_user_annotation):
    successful = await TaskDAO.delete_task(task_id)
    if not successful:
        return UserException(
            detail="No such task", status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"message": "successful"}


@router.put("/{task_id}/status")
async def change_status(
    task_id: int, status_model: TaskStatus, user: current_user_annotation
):
    updated_task = await TaskDAO.update(task_id, values_to_update=status_model)
    if not updated_task:
        return UserException(
            detail="No such task", status_code=status.HTTP_400_BAD_REQUEST
        )
    return updated_task


@router.put("/{task_id}/priority")
async def change_status(
    task_id: int, priority_model: TaskPriority, user: current_user_annotation
):
    updated_task = await TaskDAO.update(task_id, values_to_update=priority_model)
    if not updated_task:
        return UserException(
            detail="No such task", status_code=status.HTTP_400_BAD_REQUEST
        )
    return updated_task
