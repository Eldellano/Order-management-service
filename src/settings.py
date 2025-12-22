import os

from pydantic_settings import BaseSettings
from pydantic import SecretStr, EmailStr, HttpUrl, field_validator
from enum import Enum
from typing import Optional


class Config(BaseSettings):
    postgres_host: str = '127.0.0.1'
    postgres_port: int = 5432
    postgres_user: str = 'postgres'
    postgres_pass: str = '<PASSWORD>'
    postgres_db: str = 'db_name'

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    redis_user: str = 'redis'
    redis_pass: str = "<PASSWORD>"

    redis_cache_ttl: int = 60*5

    kafka_host: str = '127.0.0.1'
    kafka_port: int = 9092
    kafka_topic: str = 'order_management_service'

    app_host: str = '127.0.0.1'
    app_port: int = 8000
    app_admin_pass: str = "<PASSWORD>"


    secret_key: str = "SUPER_SECRET_KEY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30



    class Config:
        # динамическое вычисление расположения .env, для совместимости с alembic
        env_file = os.path.join(os.path.dirname(__file__), '../.env')
        env_file_encoding = 'utf-8'


settings = Config()
