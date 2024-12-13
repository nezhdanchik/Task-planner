from functools import partial

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.api.endpoints.account import current_user_annotation
from app.api.endpoints.user import get_tasks

# templates = Jinja2Templates(directory="../../../frontend/templates")
templates = Jinja2Templates(directory="./frontend/templates")

router = APIRouter()


@router.get("/register/")
async def get_register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", {"request": request, "title": "Регистрация"}
    )


@router.get("/login/")
async def get_login_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "title": "Вход"}
    )


@router.get("/main/")
async def get_main_page(
    request: Request,
    user: current_user_annotation,
    tasks_created=Depends(partial(get_tasks, status="created")),
    tasks_in_progress=Depends(partial(get_tasks, status="in_progress")),
    tasks_completed=Depends(partial(get_tasks, status="completed")),
):
    names_status = ["созданы", "в процессе", "завершены"]
    # [created [] -- in_progress [] -- completed []]
    all_tasks = []
    for ind, task_kind in enumerate(
        (tasks_created, tasks_in_progress, tasks_completed)
    ):
        tasks_one_kind = await task_kind
        tasks = {"name_status": names_status[ind], "tasks_one_kind": tasks_one_kind.get("tasks")}
        all_tasks.append(tasks)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Главная",
            "name": user.name,
            "all_tasks": all_tasks,
        },
    )


@router.get("/task/create/")
async def get_create_task_page(request: Request, user: current_user_annotation):
    return templates.TemplateResponse(
        "new_task.html",
        {"request": request, "title": "Создание задачи", "name": user.name},
    )
