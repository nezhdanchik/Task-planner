from endpoints.account import current_user_annotation
from fastapi import APIRouter

from interaction import TaskDAO
from schemas import IdModel
from schemas.task_schema import TaskStatusPriority
router = APIRouter()


@router.get("/tasks/")
async def get_tasks(
    user: current_user_annotation, status: str = "created", priority: str = "low"
):
    # class FilterModel(TaskStatusPriority, IdModel):
    #     pass
    #
    # tasks = await TaskDAO.get_all(filters=FilterModel(
    #     id=user.id,
    #     status=status,
    #     priority=priority,
    # ))
    return {"status": status, "priority": priority}
