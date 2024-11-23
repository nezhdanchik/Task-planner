from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.schemas.enums import TaskPriority, TaskStatus
from app.db.database import BaseTable, not_none_str, str_uniq


class Task(BaseTable):
    title: Mapped[not_none_str]
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    finished: Mapped[datetime] = mapped_column(default=None, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    status: Mapped[TaskStatus]
    priority: Mapped[TaskPriority]

    user: Mapped["User"] = relationship("User", back_populates="tasks")


class User(BaseTable):
    login: Mapped[str_uniq]
    password: Mapped[str]
    name: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", cascade="all, delete-orphan"
    )
