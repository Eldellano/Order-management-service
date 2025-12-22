from uuid import UUID

from fastapi import APIRouter, Depends, Response

from api.auth import get_current_user
from api.cache import get_cache, save_cache
from api.db_requests import db_requests_order as db_requests
from api.pydantic_models import order_models as pydantic_models
from api.pydantic_models.validators import ValidationError
from api.schemas import (
    ServerErrorResponse400,
    ServerErrorResponse404,
    ServerErrorResponse500,
    ServerResponse,
)
from connectors.kafka import send_kafka_message

order_router = APIRouter(prefix="/orders", tags=["order_api"])


@order_router.post(
    "/",
    summary="Создание заказа",
    responses={
        200: {"model": ServerResponse[pydantic_models.OrderResponse]},
        400: {"model": ServerErrorResponse400},
        404: {"model": ServerErrorResponse404},
        500: {"model": ServerErrorResponse500},
    },
)
async def create_order(
    response: Response,
    request: pydantic_models.OrderCreate,
    current_user: dict = Depends(get_current_user),
) -> ServerResponse:
    """Создание заказа"""
    response.status_code = 200

    try:
        user_id = current_user.get("id")
        items_dict = [item.model_dump() for item in request.items]

        new_order = await db_requests.create_order(
            user_id=user_id,
            items=items_dict,
            total_price=request.total_price,
        )

        if new_order:
            await send_kafka_message(
                key="new_order", message=new_order
            )  # запись заказа в kafka

            return ServerResponse(
                data=pydantic_models.OrderResponse(**new_order),
                success=True,
                message="Заказ создан",
                status=200,
            )
        else:
            return ServerResponse(
                data=None,
                success=False,
                message="Ошибка при создании заказа",
                status=500,
            )

    except ValueError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=404)
    except ValidationError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=400)
    except Exception as e:
        return ServerResponse(data=None, success=False, message=str(e), status=500)


@order_router.get(
    "/{order_id}/",
    summary="Получение заказа",
    responses={
        200: {"model": ServerResponse[pydantic_models.OrderResponse]},
        400: {"model": ServerErrorResponse400},
        404: {"model": ServerErrorResponse404},
        500: {"model": ServerErrorResponse500},
    },
)
async def get_order(
    response: Response,
    order_id: UUID,
) -> ServerResponse:
    """Получение заказа по id"""

    response.status_code = 200

    cache_key = f"order:{order_id}"

    try:
        order = await get_cache(cache_key)  # получения из кэша
        if not order:
            order = await db_requests.get_order(order_id)

        await save_cache(cache_key, order)  # сохранение кэша

        if not order:
            return ServerResponse(
                data=None,
                success=False,
                message="Заказ не найден",
                status=404,
            )

        return ServerResponse(
            data=pydantic_models.OrderResponse(**order),
            success=True,
            message="Заказ получен",
            status=200,
        )

    except ValueError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=404)
    except ValidationError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=400)
    except Exception as e:
        return ServerResponse(data=None, success=False, message=str(e), status=500)


@order_router.patch(
    "/{order_id}/",
    summary="Обновление статуса заказа",
    responses={
        200: {"model": ServerResponse[pydantic_models.OrderResponse]},
        400: {"model": ServerErrorResponse400},
        404: {"model": ServerErrorResponse404},
        500: {"model": ServerErrorResponse500},
    },
)
async def update_order_status(
    response: Response,
    order_id: UUID,
    request: pydantic_models.OrderUpdate,
) -> ServerResponse:
    """Обновление статуса заказа"""
    response.status_code = 200

    try:
        order = await db_requests.update_order_status(order_id, request.status)

        cache_key = f"order:{order_id}"
        await save_cache(cache_key, order)  # обновление кэша

        if not order:
            return ServerResponse(
                data=None,
                success=False,
                message="Заказ не найден",
                status=404,
            )

        return ServerResponse(
            data=pydantic_models.OrderResponse(**order),
            success=True,
            message="Статус заказа обновлен",
            status=200,
        )

    except ValueError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=404)
    except ValidationError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=400)
    except Exception as e:
        return ServerResponse(data=None, success=False, message=str(e), status=500)


@order_router.get(
    "/user/{user_id}/",
    summary="Получение заказов пользователя",
    responses={
        200: {"model": ServerResponse[list[pydantic_models.OrderResponse]]},
        400: {"model": ServerErrorResponse400},
        404: {"model": ServerErrorResponse404},
        500: {"model": ServerErrorResponse500},
    },
)
async def get_user_orders(
    response: Response,
    user_id: UUID,
) -> ServerResponse:
    """Получение всех заказов пользователя"""
    response.status_code = 200

    try:
        orders = await db_requests.get_user_orders(user_id)

        orders_list = [pydantic_models.OrderResponse(**order) for order in orders]

        return ServerResponse(
            data=orders_list,
            success=True,
            message="Заказы получены",
            status=200,
        )

    except ValueError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=404)
    except ValidationError as ve:
        return ServerResponse(data=None, success=False, message=str(ve), status=400)
    except Exception as e:
        return ServerResponse(data=None, success=False, message=str(e), status=500)

