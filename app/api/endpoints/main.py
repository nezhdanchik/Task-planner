from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.account import router as account_router
from app.api.endpoints.pages import router as page_router
from app.api.endpoints.task import router as task_router
from app.api.endpoints.user import router as user_router
from app.api.exceptions import *

from app.db.database import are_tables_exist, create_tables, is_database_exist, create_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not await is_database_exist():
        await create_database()

    if not await are_tables_exist():
        await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/assets", StaticFiles(directory="./frontend/assets"), name="assets")


@app.exception_handler(UserException)
async def custom_exception_handler(request, exc):
    error = CustomExceptionModel(status_code=exc.status_code,
                                 er_details=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=error.model_dump())


@app.exception_handler(TaskException)
async def custom_exception_handler(request, exc):
    error = CustomExceptionModel(status_code=exc.status_code,
                                 er_details=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=error.model_dump())


@app.get("/")
async def root():
    return {"message": "hello"}


app.include_router(task_router, prefix="/task", tags=["task"])
app.include_router(account_router, prefix="/account", tags=["account"])
app.include_router(page_router, prefix="/page", tags=["page"])
app.include_router(user_router, prefix="/user", tags=["user"])

# if __name__ == "__main__":
#     import uvicorn
#     app.mount("/assets", StaticFiles(directory="../../../frontend/assets"), name="assets")
#     uvicorn.run(app, port=8000)
