from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import create_access_token, verify_password
from api.db_requests import db_requests_user as db_requests
from api.pydantic_models import user_models as pydantic_models
from api.pydantic_models.validators import ValidationError
from api.schemas import (
    ServerErrorResponse400,
    ServerErrorResponse404,
    ServerErrorResponse500,
    ServerResponse,
)

user_router = APIRouter(prefix="/user", tags=["user_api"])


@user_router.post(
    "/register",
    summary="Регистрация пользователя",
    responses={
        200: {"model": ServerResponse[pydantic_models.UserResponse]},
        400: {"model": ServerErrorResponse400},
        404: {"model": ServerErrorResponse404},
        500: {"model": ServerErrorResponse500},
    },
)
async def user_registry(
    response: Response, request: pydantic_models.UserCreate
) -> ServerResponse:
    response.status_code = 200

    try:
        email = request.email
        password = request.password

        if await db_requests.check_user_email(email):
            return ServerResponse(
                data=None,
                success=False,
                message="Пользователь с таким email уже существует",
                status=200,
            )

        new_user = await db_requests.add_user(
            email=email,
            password=password,
        )

        if new_user:
            return ServerResponse(
                data=pydantic_models.UserResponse(**new_user),
                success=True,
                message="create",
                status=200,
            )
        else:
            return ServerResponse(
                data=None, success=False, message="something wrong", status=500
            )

    except ValueError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=404)
    except ValidationError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=400)
    except Exception as e:
        return ServerResponse(data=None, success=False, message=str(e), status=500)


@user_router.post(
    "/token/",
    summary="Получение токена доступа",
    responses={
        200: {"model": ServerResponse[pydantic_models.TokenResponse]},
        400: {"model": ServerErrorResponse400},
        404: {"model": ServerErrorResponse404},
        500: {"model": ServerErrorResponse500},
    },
)
async def get_token(
    response: Response, request: OAuth2PasswordRequestForm = Depends()
) -> ServerResponse:
    try:
        user_email = request.username
        user = await db_requests.get_user(user_email)

        if not user or not await verify_password(
            request.password, user.get("hashed_password")
        ):
            return ServerResponse(
                data=None,
                success=False,
                message="Incorrect email or password",
                status=500,
            )
        else:
            access_token = await create_access_token({"sub": user.get("email")})

            return ServerResponse(
                data=pydantic_models.TokenResponse(access_token=access_token),
                success=True,
                message="create",
                status=200,
            )

    except ValueError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=404)
    except ValidationError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=400)
    except Exception as e:
        return ServerResponse(data=None, success=False, message=str(e), status=500)
