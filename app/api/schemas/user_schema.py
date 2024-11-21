from datetime import datetime

from pydantic import BaseModel, Field


class UserOnlyLogin(BaseModel):
    login: str = Field(min_length=3, max_length=20)


class UserCreate(UserOnlyLogin):
    password: str = Field(min_length=5, max_length=200)
    name: str = Field(min_length=1, max_length=20)


class UserIn(UserOnlyLogin):
    password: str


class UserOut(UserOnlyLogin):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
