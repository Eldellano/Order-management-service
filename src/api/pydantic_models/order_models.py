from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from db_models.db_models import OrderStatus


class OrderItem(BaseModel):
    """Модель товара в заказе"""

    name: str = Field(description="Название товара")
    quantity: int = Field(description="Количество")
    price: float = Field(description="Цена за единицу")


class OrderCreate(BaseModel):
    """Модель для создания заказа"""

    items: List[OrderItem] = Field(description="Список товаров")
    total_price: float = Field(description="Общая стоимость")


class OrderUpdate(BaseModel):
    """Модель для обновления статуса заказа"""

    status: OrderStatus = Field(description="Статус заказа")


class OrderResponse(BaseModel):
    """Модель ответа с данными заказа"""

    id: UUID = Field(description="id заказа")
    user_id: UUID = Field(description="id пользователя")
    items: list[dict] = Field(description="Список товаров")
    total_price: float = Field(description="Общая стоимость")
    status: str = Field(description="Статус заказа")
    created_at: datetime = Field(description="Время создания")

