from endpoints.account import current_user_annotation
from fastapi import APIRouter

from interaction import TaskDAO
from schemas import IdModel
from schemas.task_schema import TaskStatus
router = APIRouter()


@router.get("/tasks/")
async def get_tasks(
    user: current_user_annotation, status: str = "created"):
    #валидация статуса
    TaskStatus(status=status)
    tasks = await TaskDAO.get_all_tasks_with_status(
        user_id=user.id,
        status=status
    )
    return tasks
