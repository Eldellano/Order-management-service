from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Почта пользователя")
    password: str = Field(description="Пароль")


class UserResponse(BaseModel):
    email: EmailStr = Field(description="Почта пользователя")
    created_at: datetime = Field(description="Время создания")


class TokenResponse(BaseModel):
    access_token: str = Field(description="Токен доступа")
    token_type: str = "bearer"