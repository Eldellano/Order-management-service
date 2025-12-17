from pydantic import EmailStr
from sqlalchemy.future import select

from api.auth import hash_password
from connectors.orm import db
from db_models import db_models


async def check_user_email(email: EmailStr) -> dict | None:
    """Проверка существования пользователя с переданным email"""

    if email == "":
        raise ValueError("empty-email")

    async with db.AsyncSession() as session:
        query = select(db_models.User).where(db_models.User.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            user_dict = {c.name: getattr(user, c.name) for c in user.__table__.columns}
            return user_dict
        return None


async def add_user(
    email: EmailStr,
    password: str,
):
    """Сохранение нового пользователя"""

    hashed_password = await hash_password(password)
    new_user = db_models.User(
        email=email,
        hashed_password=hashed_password,
    )

    async with db.AsyncSession() as session:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        data_for_return = {
            c.name: getattr(new_user, c.name)
            for c in new_user.__table__.columns
            if c.name != "hashed_password"
        }

        return data_for_return


async def get_user(user_email: str) -> dict | None:
    """Получение данных пользователя"""

    async with db.AsyncSession() as session:
        query = select(db_models.User).where(db_models.User.email == user_email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError(f"Запись для {user_email} не найдена.")

        user_result = {c.name: getattr(user, c.name) for c in user.__table__.columns}

        return user_result