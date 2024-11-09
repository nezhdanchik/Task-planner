from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from session_maker import connection
from models import TaskTable
from app.api.schemas.task_schema import Task, TaskInDB


@connection()
async def add_task(task: Task, return_pydantic=False, session: AsyncSession = ...):
    task_dict = task.model_dump(exclude_unset=True)
    new_task = TaskTable(**task_dict)
    session.add(new_task)
    await session.flush()
    if return_pydantic:
        return TaskInDB.model_validate(new_task, from_attributes=True)
    return new_task


@connection(commit=False)
async def get_task(task_id: int, return_pydantic=False, session: AsyncSession = ...):
    task = await session.get(TaskTable, task_id)
    if not task:
        return None
    if return_pydantic:
        return TaskInDB.model_validate(task, from_attributes=True)
    return task


@connection(commit=False)
async def get_tasks(filters: BaseModel | None = None,
                    return_pydantic=False,
                    session: AsyncSession = ...):
    if filters:
        filter_dict = filters.model_dump(exclude_unset=True)
    else:
        filter_dict = {}
    tasks = await session.execute(select(TaskTable).filter_by(**filter_dict))
    tasks = tasks.scalars().all()
    if return_pydantic:
        return [TaskInDB.model_validate(task, from_attributes=True) for task in tasks]
    return tasks


@connection(commit=True)
async def update_task(task_id: int, values: BaseModel,
                      return_pydantic: bool = False,
                      session: AsyncSession = ...):
    values_dict = values.model_dump(exclude_unset=True)
    target_task = await session.get(TaskTable, task_id)
    for key, value in values_dict.items():
        setattr(target_task, key, value)
    if return_pydantic:
        return TaskInDB.model_validate(target_task, from_attributes=True)
    return target_task


@connection(commit=True)
async def delete_task(task_id: int, session: AsyncSession = ...):
    """
    :return: True - если удаление произошло успешно
    """
    target_task = await session.get(TaskTable, task_id)
    if not target_task:
        return False
    await session.delete(target_task)
    return True
