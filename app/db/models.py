from sqlalchemy.orm import Mapped, mapped_column

from database import (
    BaseTable,
    not_none_str,
)

class TaskTable(BaseTable):
    title: Mapped[not_none_str]
    description: Mapped[not_none_str]
    completed: Mapped[bool] = mapped_column(default=False)