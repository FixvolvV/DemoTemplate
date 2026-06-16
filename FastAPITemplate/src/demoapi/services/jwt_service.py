from datetime import datetime, timedelta, UTC
from typing import Any

import bcrypt
import jwt
from pydantic import BaseModel

from demoapi.core.settings import (
    settings,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
)


class UserJwt(BaseModel):

    id: str
    role: str


class TokenInfo(BaseModel):

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


def hash_password(password: str) -> str:
    """Хэширует пароль с использованием bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def validate_password(password: str, hashed: str) -> bool:
    """Проверяет пароль против хэша."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def encode_jwt(
    payload: dict[str, Any],
    expires_minutes: int | None = None,
    expires_days: int | None = None,
) -> str:

    now = datetime.now(UTC)

    # Вычисляем время истечения
    if expires_days is not None:
        expire = now + timedelta(days=expires_days)
    elif expires_minutes is not None:
        expire = now + timedelta(minutes=expires_minutes)
    else:
        expire = now + timedelta(minutes=settings.jwt.access_token_expire_minutes)

    # Формируем полный payload
    to_encode = payload.copy()
    to_encode.update(
        {
            "iat": now,
            "exp": expire,
        }
    )

    # Подписываем токен с PyJWT
    token = jwt.encode(
        to_encode,
        settings.jwt.private.read_text(),
        algorithm=settings.jwt.algorithm,
    )

    return token


def decode_jwt(token: str) -> dict[str, Any]:

    try:
        payload = jwt.decode(
            token,
            settings.jwt.public.read_text(),
            algorithms=[settings.jwt.algorithm],  # Фиксированный алгоритм
        )
        return payload
    except jwt.InvalidTokenError as e:
        raise


def create_access_token(user: UserJwt) -> str:
    """
    Создаёт access-токен для пользователя.

    Payload:
    - sub: user.id
    - role: user.role
    - type: "access"
    """
    payload = {
        "sub": user.id,
        "role": user.role,
        TOKEN_TYPE_FIELD: ACCESS_TOKEN_TYPE,
    }

    token = encode_jwt(
        payload, expires_minutes=settings.jwt.access_token_expire_minutes
    )

    return token


def create_refresh_token(user: UserJwt) -> str:
    """
    Создаёт refresh-токен для пользователя.

    Payload:
    - sub: user.id
    - type: "refresh"
    """
    payload = {
        "sub": user.id,
        TOKEN_TYPE_FIELD: REFRESH_TOKEN_TYPE,
    }

    token = encode_jwt(payload, expires_days=settings.jwt.refresh_token_expire_days)

    return token
