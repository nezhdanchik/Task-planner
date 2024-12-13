import copy
import json
import logging

from app.api.schemas.task_schema import TaskStatus
from app.core.config import get_redis_host

from redis import asyncio as aioredis


class UserTasksCache:
    name = 'tasks'

    def __init__(self, status, user_id):
        self.status = TaskStatus(status=status).status.value
        self.user_id = user_id
        self.redis = aioredis.from_url(f"redis://{get_redis_host()}",
                                       decode_responses=True)
        self.key = self._create_key(status=self.status,
                                    user_id=self.user_id)

    @staticmethod
    def check_redis_health(func):
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logging.error(f'Ошибка с redis {e}')
                return None
        return inner

    @classmethod
    def _create_key(cls, *args, **kwargs):
        key_elems = [str(cls.name)]
        for item in args:
            key_elems.append(str(item))
        for key, value in kwargs.items():
            key_elems += [str(key), str(value)]
        return ':'.join(key_elems)

    @classmethod
    def change_none_to_empty_string(cls, d: dict, change=False):
        if not change:
            d = copy.deepcopy(d)
        for key, value in d.items():
            if isinstance(value, dict):
                d[key] = cls.change_none_to_empty_string(value, change=change)
            elif value is None:
                d[key] = ''
        return d

    @check_redis_health
    async def hget(self):
        result = await self.redis.get(self.key)
        if result:
            return json.loads(result)
        return None

    @check_redis_health
    async def hset(self,
                   value: dict,
                   time: int | None = None,
                   change_none_in_value=False):
        prepared = self.change_none_to_empty_string(value,
                                                    change=change_none_in_value)
        serialized_value = json.dumps(prepared)
        return await self.redis.set(self.key, serialized_value, time)

    @check_redis_health
    async def delete(self):
        return await self.redis.delete(self.key)
