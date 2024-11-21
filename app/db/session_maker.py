from functools import wraps

from database import async_session_maker
from sqlalchemy import text


def connection(isolation_level: str | None = None, commit: bool = True):
    """
    Декоратор для управления сессией с возможностью настройки уровня изоляции и коммита.
    :param isolation_level: Уровень изоляции для транзакции (например, "SERIALIZABLE").
    :param commit: Если `True`, выполняется коммит после вызова метода.
    """

    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    if isolation_level:
                        await session.execute(
                            text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
                        )
                    result = await method(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()

        return wrapper

    return decorator
