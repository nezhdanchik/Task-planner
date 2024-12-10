import asyncio
from datetime import datetime
from typing import Annotated

from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, \
    create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.core.config import get_db_url, get_postgres_db_url
from core.config import get_db_name

DATABASE_URL = get_db_url()
DATABASE_NAME = get_db_name()
DATABASE_POSTGRES_URL = get_postgres_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

engine_postgres_db = create_async_engine(DATABASE_POSTGRES_URL, isolation_level="AUTOCOMMIT")

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
not_none_str = Annotated[str, mapped_column(nullable=False)]


class BaseTable(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


async def is_database_exist():
    async with engine_postgres_db.connect() as conn:
        res = await conn.execute(text(
            f"""
            SELECT datname FROM pg_catalog.pg_database
            WHERE lower(datname) = lower('{DATABASE_NAME}');
            """
        ))
        return bool(res.first())

async def create_database():
    print('Creating database')
    async with engine_postgres_db.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE {DATABASE_NAME}"))
    print('Database created')


async def are_tables_exist():
    async with async_session_maker() as session:
        res = await session.execute(text(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema='public';
            """
        ))
        return bool(res.all())


async def create_tables():
    print('Creating tables')
    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)
    print('Tables created')

