from uuid import UUID

from sqlalchemy.future import select

from connectors.orm import db
from db_models import db_models


async def create_order(
    user_id: UUID,
    items: list,
    total_price: float,
    status: db_models.OrderStatus = db_models.OrderStatus.PENDING,
) -> dict:
    """Создание нового заказа"""

    new_order = db_models.Order(
        user_id=user_id,
        items=items,
        total_price=total_price,
        status=status,
    )

    async with db.AsyncSession() as session:
        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)

        data_for_return = {
            c.name: getattr(new_order, c.name) for c in new_order.__table__.columns
        }

        return data_for_return


async def get_order(order_id: UUID) -> dict | None:
    """Получение заказа по id"""

    async with db.AsyncSession() as session:
        query = select(db_models.Order).where(db_models.Order.id == order_id)
        result = await session.execute(query)
        order = result.scalar_one_or_none()

        if not order:
            return None

        order_result = {c.name: getattr(order, c.name) for c in order.__table__.columns}

        return order_result


async def update_order_status(
    order_id: UUID, status: db_models.OrderStatus
) -> dict | None:
    """Обновление статуса заказа"""

    async with db.AsyncSession() as session:
        query = select(db_models.Order).where(db_models.Order.id == order_id)
        result = await session.execute(query)
        order = result.scalar_one_or_none()

        if not order:
            return None

        order.status = status
        await session.commit()
        await session.refresh(order)

        order_result = {c.name: getattr(order, c.name) for c in order.__table__.columns}

        return order_result


async def get_user_orders(user_id: UUID) -> list[dict]:
    """Получение всех заказов пользователя"""

    async with db.AsyncSession() as session:
        query = select(db_models.Order).where(db_models.Order.user_id == user_id)
        result = await session.execute(query)
        orders = result.scalars().all()

        orders_list = []
        for order in orders:
            order_dict = {
                c.name: getattr(order, c.name) for c in order.__table__.columns
            }
            orders_list.append(order_dict)

        return orders_list

