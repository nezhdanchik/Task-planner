from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from api.endpoints.account import current_user_annotation

templates = Jinja2Templates(directory="../../../frontend/templates")

router = APIRouter()


@router.get("/register/")
async def get_register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", {"request": request, "title": "Регистрация"}
    )


@router.get("/login/")
async def get_register_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "title": "Вход"}
    )


@router.get("/main/")
async def get_main_page(request: Request, user: current_user_annotation):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Главная", "name": user.name}
    )


@router.get("/task/create/")
async def get_create_task_page(request: Request, user: current_user_annotation):
    return templates.TemplateResponse(
        "new_task.html",
        {"request": request, "title": "Создание задачи", "name": user.name},
    )
