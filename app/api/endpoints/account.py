from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from api.exceptions import *
from db.interaction import UserDAO
from fastapi import APIRouter, Depends, Request, Response, status
from schemas.user_schema import UserCreate, UserIn, UserOnlyLogin, UserOut
from sqlalchemy.exc import IntegrityError

from app.core.config import get_algorithm, get_secret_key

router = APIRouter()
LIFE_TIME = timedelta(days=100)
SECRET_KEY = get_secret_key()
ALGORITHM = get_algorithm()


def create_jwt_token(data: dict) -> str:
    data.update({"exp": datetime.timestamp(datetime.now() + LIFE_TIME)})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def set_token_in_cookie(response: Response, token: str):
    response.set_cookie("access_token", token, httponly=True)


def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise UserException(
            detail="Token not found", status_code=status.HTTP_401_UNAUTHORIZED
        )
    return token


async def get_current_user(token: str = Depends(get_token_from_cookie)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        user = await UserDAO.get_one_or_none(obj_id=id)
        if not user:
            raise UserException(detail="User does not exist", status_code=400)
        return user
    except jwt.ExpiredSignatureError:
        raise UserException(
            detail="Not authenticated", status_code=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        raise UserException(
            detail="Invalid token", status_code=status.HTTP_400_BAD_REQUEST
        )


current_user_annotation = Annotated[UserOut, Depends(get_current_user)]


@router.post(
    "/register/",
    responses={
        status.HTTP_200_OK: {"model": UserOut},
        status.HTTP_400_BAD_REQUEST: {"model": CustomExceptionModel},
    },
)
async def create_user(user: UserCreate) -> UserOut:
    try:
        user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
        new_user = await UserDAO.create(user)
    except IntegrityError:
        raise UserException(detail="User already exists", status_code=400)
    else:
        return new_user


@router.post("/login/")
async def enter_user(user: UserIn, response: Response) -> dict:
    user_in_db = await UserDAO.get_one_or_none_by(UserOnlyLogin(login=user.login))
    if not user_in_db:
        raise UserException(detail="User does not exist", status_code=400)
    valid = bcrypt.checkpw(user.password.encode(), user_in_db.password.encode())
    if not valid:
        raise UserException(detail="Invalid password", status_code=400)
    access_token = create_jwt_token({"sub": user_in_db.id})
    set_token_in_cookie(response=response, token=access_token)
    return {
        "access_token": access_token,
    }


@router.get("/logout/")
async def exit_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "successful"}


@router.get("/me/")
async def get_me(user: current_user_annotation):
    return user
