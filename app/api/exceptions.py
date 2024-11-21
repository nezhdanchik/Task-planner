from fastapi import HTTPException
from pydantic import BaseModel


class CustomExceptionModel(BaseModel):
    status_code: int
    er_details: str


# -------------------- User exceptions --------------------


class UserException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


# -------------------- Task exceptions --------------------


class TaskException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)
