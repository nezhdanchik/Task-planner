import asyncio

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.enums import TaskPriority, TaskStatus
from app.api.schemas.task_schema import TaskCreate
from app.db.database import BaseTable

from app.db.models import Task as TaskTable, User as UserTable
from app.db.session_maker import connection


class BaseDAO:
    Table: BaseTable

    @classmethod
    @connection()
    async def create(
        cls, adding_obj: BaseModel, exclude_unset=True, session: AsyncSession = ...
    ):
        adding_obj_dict = adding_obj.model_dump(exclude_unset=exclude_unset)
        new_obj = cls.Table(**adding_obj_dict)
        session.add(new_obj)
        await session.flush()
        return new_obj

    @classmethod
    @connection(commit=False)
    async def get_one_or_none(cls, obj_id: int, session: AsyncSession = ...):
        obj = await session.get(cls.Table, obj_id)
        if not obj:
            return None
        return obj

    @classmethod
    @connection(commit=False)
    async def get_all(
        cls,
        filters: BaseModel | None = None,
        exclude_unset=True,
        session: AsyncSession = ...,
    ):
        if filters:
            filter_dict = filters.model_dump(exclude_unset=exclude_unset)
        else:
            filter_dict = {}
        objs = await session.execute(select(cls.Table).filter_by(**filter_dict))
        objs = objs.scalars().all()
        return objs

    @classmethod
    @connection(commit=False)
    async def get_one_or_none_by(
        cls,
        filters: BaseModel | None = None,
        exclude_unset=True,
        session: AsyncSession = ...,
    ):
        if filters:
            filter_dict = filters.model_dump(exclude_unset=exclude_unset)
        else:
            filter_dict = {}
        objs = await session.execute(select(cls.Table).filter_by(**filter_dict))
        objs = objs.scalars().first()
        return objs

    @classmethod
    @connection(commit=True)
    async def update(
        cls,
        obj_id: int,
        values_to_update: BaseModel,
        exclude_unset=True,
        session: AsyncSession = ...,
    ):
        values_dict = values_to_update.model_dump(exclude_unset=exclude_unset)
        target_obj = await session.get(cls.Table, obj_id)
        if not target_obj:
            return
        for key, value in values_dict.items():
            setattr(target_obj, key, value)
        return target_obj

    @classmethod
    @connection(commit=True)
    async def delete_task(cls, obj_id: int, session: AsyncSession = ...):
        """
        :return: True - если удаление произошло успешно
        """
        target_obj = await session.get(cls.Table, obj_id)
        if not target_obj:
            return False
        await session.delete(target_obj)
        return True


class UserDAO(BaseDAO):
    Table = UserTable


class TaskDAO(BaseDAO):
    Table = TaskTable

    @classmethod
    @connection(commit=True)
    async def create(
        cls,
        task: BaseModel,
        user_id: int,
        exclude_unset=True,
        session: AsyncSession = ...,
    ):
        adding_obj_dict = task.model_dump(exclude_unset=exclude_unset)
        adding_obj_dict["user_id"] = user_id
        new_obj = cls.Table(**adding_obj_dict)
        session.add(new_obj)
        await session.flush()
        return new_obj

    # конфликт
    # @classmethod
    # @connection(commit=True)
    # async def change_status(cls, task_id, new_status: TaskStatus, session: AsyncSession):
    #     """
    #     :return: None - если обновление не произошло
    #     """
    #     # task = await cls.get_one_or_none(task_id) # почему-то не работает. видимо какой-то конфликт с сессией
    #     task = await session.get(cls.Table, task_id)
    #     if not task:
    #         return False
    #     task.status = new_status
    #     return task

    @classmethod
    @connection(commit=False)
    async def get_all_tasks_with_status(
        cls,
        user_id: int,
        status: str = TaskStatus.CREATED.value,
        session: AsyncSession = ...,
    ):
        objs = await session.execute(
            select(cls.Table)
            .filter_by(status=status, user_id=user_id)
            .order_by(cls.Table.priority.desc(), cls.Table.created_at)
        )
        objs = objs.scalars().all()
        return objs


if __name__ == "__main__":
    user_id = 1
    fake_tasks = [
        TaskCreate(
            title="Позвонить стоматологу",
            description="Записаться на осмотр на следующую неделю",
            priority=TaskPriority.HIGH,
            status=TaskStatus.CREATED,
        ),
        TaskCreate(
            title="Проверить почту",
            description="Ответить на важные письма",
            priority=TaskPriority.LOW,
            status=TaskStatus.IN_PROGRESS,
        ),
        TaskCreate(
            title="Выгулять собаку",
            description="Пройтись в парке 30 минут",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.COMPLETED,
        ),
        TaskCreate(
            title="Пропылесосить ковёр",
            description="Убрать грязь и пыль в гостиной",
            priority=TaskPriority.HIGH,
            status=TaskStatus.CREATED,
        ),
        TaskCreate(
            title="Прочитать книгу",
            description="Закончить последнюю главу книги",
            priority=TaskPriority.LOW,
            status=TaskStatus.IN_PROGRESS,
        ),
        TaskCreate(
            title="Посетить спортзал",
            description="Сделать силовую тренировку",
            priority=TaskPriority.HIGH,
            status=TaskStatus.CREATED,
        ),
        TaskCreate(
            title="Полить цветы",
            description="Полить растения в гостиной и на балконе",
            priority=TaskPriority.LOW,
            status=TaskStatus.COMPLETED,
        ),
        TaskCreate(
            title="Составить список покупок",
            description="Подготовить список на неделю",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.CREATED,
        ),
        TaskCreate(
            title="Оплатить счета",
            description="Заплатить за интернет и электричество",
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS,
        ),
        TaskCreate(
            title="Убрать на рабочем столе",
            description="Разложить бумаги по папкам и вытереть пыль",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.CREATED,
        ),
        TaskCreate(
            title="Написать отчёт",
            description="Подготовить отчёт по проекту за месяц",
            priority=TaskPriority.HIGH,
            status=TaskStatus.IN_PROGRESS,
        ),
        TaskCreate(
            title="Проверить состояние машины",
            description="Проверить уровень масла и давления в шинах",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.CREATED,
        ),
        TaskCreate(
            title="Сделать уборку на кухне",
            description="Протереть все поверхности и вымыть пол",
            priority=TaskPriority.HIGH,
            status=TaskStatus.CREATED,
        ),
    ]

    async_tasks = [TaskDAO.create(task, user_id) for task in fake_tasks]

    async def main():
        await asyncio.gather(*async_tasks)

    asyncio.run(main())
