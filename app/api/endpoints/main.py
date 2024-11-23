from api.exceptions import *
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.account import router as account_router
from app.api.endpoints.pages import router as page_router
from app.api.endpoints.task import router as task_router
from app.api.endpoints.user import router as user_router

app = FastAPI()
app.mount("/assets", StaticFiles(directory="../../../frontend/assets"), name="assets")

# @app.exception_handler(RequestValidationError)
# async def custom_request_validation_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=422,
#         content={"message": "Custom Request Validation Error", "errors": exc.errors()},
#     )


@app.exception_handler(UserException)
async def custom_exception_handler(request, exc):
    error = CustomExceptionModel(status_code=exc.status_code, er_details=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=error.model_dump())


@app.exception_handler(TaskException)
async def custom_exception_handler(request, exc):
    error = CustomExceptionModel(status_code=exc.status_code, er_details=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=error.model_dump())


app.include_router(task_router, prefix="/task", tags=["task"])
app.include_router(account_router, prefix="/account", tags=["account"])
app.include_router(page_router, prefix="/page", tags=["page"])
app.include_router(user_router, prefix="/user", tags=["user"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
