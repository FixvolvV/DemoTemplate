from typing import Annotated

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from demoapi.core.postgesql import postgres

from demoapi.core.settings import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from .jwt_service import decode_jwt, validate_password

from shoersshopapi.api.v1.users.crud import UserCrud  # TODO: Вставить рабочий crud


# Константы ошибок

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)

FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden",
)

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
)

CONFLICT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Already exists",
)

NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found",
)


# OAuth2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

http_bearer = HTTPBearer(auto_error=False)

# Утилиты валидации токена


def is_email(value: str) -> bool:
    return "@" in value


def get_current_token_payload(token: str) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise UNAUTHORIZED
    return payload


def validate_token_type(payload: dict, expected_type: str) -> None:
    if payload.get(TOKEN_TYPE_FIELD) != expected_type:
        raise UNAUTHORIZED


async def get_user_by_token_sub(
    payload: dict,
    session: AsyncSession,
):
    user_id: str | None = payload.get("sub")
    if not user_id:
        raise UNAUTHORIZED

    user = await UserCrud.get_by_id(session=session, user_id=user_id)
    if not user:
        raise UNAUTHORIZED

    return user


# Валидация логина


async def validate_auth_user(
    session: Annotated[
        AsyncSession,
        Depends(postgres.get_session),
    ],
    login: str = Form(),
    password: str = Form(),
):

    user = await UserCrud.get_by_login(session=session, login=login)

    if not user:
        raise INVALID_CREDENTIALS

    if not validate_password(password, user.password):
        raise INVALID_CREDENTIALS

    return user


# Получение текущего пользователя из токена


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[
            AsyncSession,
            Depends(postgres.get_session),
        ],
    ):
        payload = get_current_token_payload(token)
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload, session)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


# Проверка ролей


class RoleRequired:

    def __init__(self, *allowed_roles: str):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[
            AsyncSession,
            Depends(postgres.get_session),
        ],
    ):
        payload = get_current_token_payload(token)
        validate_token_type(payload, ACCESS_TOKEN_TYPE)
        user = await get_user_by_token_sub(payload, session)

        if user.role not in self.allowed_roles:
            raise FORBIDDEN

        return user
