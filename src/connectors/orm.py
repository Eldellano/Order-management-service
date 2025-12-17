from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.settings import settings


class Database:
    def __init__(self):
        self.postgres_host: str = settings.postgres_host
        self.postgres_port: int = settings.postgres_port
        self.postgres_user: str = settings.postgres_user
        self.postgres_pass: str = settings.postgres_pass
        self.postgres_db: str = settings.postgres_db

        self.engine = create_async_engine(
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_pass}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}",
        )

        self.AsyncSession = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False)

        self.Base = declarative_base()

    async def get_db(self):
        """Предоставляет сессию базы данных для взаимодействия."""

        async with self.AsyncSession() as session:
            yield session


db = Database()
