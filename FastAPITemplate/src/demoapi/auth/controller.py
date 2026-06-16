from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from demoapi.core.postgesql import postgres
from demoapi.core.postgesql.model import User  # TODO: после инита базы данных.

from demoapi.user.crud import UserCrud  # TODO: после создания инстанса UserCrud

from demoapi.user.schemas import UserFull  # TODO: после создания user

from demoapi.services.jwt_service import (
    UserJwt,
    TokenInfo,
    create_access_token,
    create_refresh_token,
)

from demoapi.services.http import (
    validate_auth_user,
    get_current_auth_user,
    get_current_auth_user_for_refresh,
)

from .schemas import RegisterSchema


router = APIRouter(tags=["Auth"])

USERNOTFOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

#  REGISTER


@router.post(
    "/register",
    response_model=TokenInfo,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterSchema,
    session: Annotated[AsyncSession, Depends(postgres.get_session)],
):

    user = await UserCrud.create_user(session, data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="User register failed"
        )

    jwt_user = UserJwt(
        id=user.id,
        role=user.role,
    )

    access_token = create_access_token(jwt_user)
    refresh_token = create_refresh_token(jwt_user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


#  LOGIN


@router.post(
    "/login",
    response_model=TokenInfo,
    summary="Авторизация",
)
async def login(
    user: Annotated[User, Depends(validate_auth_user)],
):

    jwt_user = UserJwt(
        id=user.id,
        role=user.role,
    )

    access_token = create_access_token(jwt_user)
    refresh_token = create_refresh_token(jwt_user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


#  REFRESH


@router.post(
    "/refresh",
    response_model=TokenInfo,
    summary="Обновить токен",
)
async def refresh_token(
    user: Annotated[User, Depends(get_current_auth_user_for_refresh)],
):
    """
    Обновить access токен по refresh токену.
    """
    jwt_user = UserJwt(
        id=user.id,
        role=user.role,
    )

    access_token = create_access_token(jwt_user)
    refresh_token = create_refresh_token(jwt_user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


#  ME


@router.get(
    "/me",
    response_model=UserFull,
    summary="Текущий пользователь",
)
async def get_me(
    user: Annotated[User, Depends(get_current_auth_user)],
    session: Annotated[AsyncSession, Depends(postgres.get_session)],
):

    user_data = await UserCrud.get_full(session, user.id)

    if not user_data:
        raise USERNOTFOUND

    return user_data
