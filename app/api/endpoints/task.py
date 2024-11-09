from fastapi import FastAPI

from api.schemas.task_schema import Task, UpdateTask
from db import interaction

app = FastAPI()


@app.post("/task/")
async def create_task(task: Task):
    return await interaction.add_task(task, return_pydantic=True)


@app.get("/task/{task_id}")
async def get_task(task_id: int):
    task = await interaction.get_task(task_id=task_id, return_pydantic=True)
    if task:
        return task
    return {"message": "no such task"}


@app.patch("/task/{task_id}")
async def update_task(task_id: int, task: UpdateTask):
    return await interaction.update_task(task_id=task_id,
                                         values=task,
                                         return_pydantic=True)


@app.delete("/task/{task_id}")
async def delete_task(task_id: int):
    if await interaction.delete_task(task_id=task_id):
        return {"message": "deleted successfully"}
    return {"message": "no such task"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
