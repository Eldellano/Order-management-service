import uuid

from sqlalchemy import (
    TIMESTAMP,
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from src.db_models.db_base import Base


class User(Base):
    __tablename__ = "user"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="id пользователя"
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="Почта пользователя")
    hashed_password: Mapped[str] = mapped_column(String(255), comment="Пароль")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=now(), comment="Время создания"
    )

