from uuid import UUID

from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from domain.user.schema import (
    UserReturnData,
    GetUserById,
    GetUserByLogin,
    CreateUser,
    UpdateUser,
    UserLogin,
    UserJwtToken,
)
from infrastructure.authentification.auth_helper import jwt_header
from infrastructure.database.models import User
from service.auth_service import AuthService
from service.user_service import UserShowService, UserDataManagerService

user_router = APIRouter(prefix="/user")


@user_router.get("/all", response_model=list[UserReturnData])
async def show_all_users(
    repository: UserShowService = Depends(UserShowService),
) -> list[User]:
    """
    Корутина возвращает список юзеров
    :param repository:
    :return:
    """
    return await repository.get_all_users()


@user_router.get("/search_id/{user_id}", response_model=UserReturnData)
async def show_user_by_id(
    user_id: UUID, repository: UserShowService = Depends(UserShowService)
) -> UserReturnData:
    """
    Корутина возвращает юзера по айди
    :param user_id:
    :param repository:
    :return:
    """
    return await repository.find_user_by_id(cmd=GetUserById(id=user_id))


@user_router.get("/search_login/{login}", response_model=UserReturnData)
async def show_user_by_login(
    login: str, repository: UserShowService = Depends(UserShowService)
) -> UserReturnData:
    """
    Корутина возвращает юзера по логину
    :param login:
    :param repository:
    :return:
    """
    return await repository.find_user_by_login(cmd=GetUserByLogin(login=login))


@user_router.post(
    "/register", response_model=UserReturnData, status_code=status.HTTP_201_CREATED
)
async def registration(
    cmd: CreateUser,
    repository: UserDataManagerService = Depends(UserDataManagerService),
) -> UserReturnData:
    """
    Корутина создает юзера
    :param cmd:
    :param repository:
    :return:
    """
    return await repository.register_user(cmd=cmd)


@user_router.patch("/upd/{user_id}", response_model=UserReturnData)
async def upd_user(
    user_id: UUID,
    cmd: UpdateUser,
    repository: UserDataManagerService = Depends(UserDataManagerService),
) -> UserReturnData:
    """
    Корутина апдейтит юзера
    :param user_id:
    :param cmd:
    :param repository:
    :return:
    """
    return await repository.change_user(cmd=cmd, model_id=GetUserById(id=user_id))


@user_router.delete("/del/{user_id}", response_model=UserReturnData)
async def del_user(
    user_id: UUID, repository: UserDataManagerService = Depends(UserDataManagerService)
) -> UserReturnData:
    """
    Корутина удаляет юзера
    :param user_id:
    :param repository:
    :return:
    """
    return await repository.drop_user(model_id=GetUserById(id=user_id))


@user_router.post("/login", response_model=None)
async def login_user(
    cmd: UserLogin, repository: AuthService = Depends(AuthService)
) -> dict[str, str]:
    """
    Корутина для логина
    :param cmd:
    :param repository:
    :return:
    """
    return await repository.login(cmd=cmd)


@user_router.post("/logout", response_model=UserJwtToken)
async def logout_user(
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
    repository: AuthService = Depends(AuthService),
) -> UserJwtToken:
    """
    Корутина для логаута
    :param credentials:
    :param repository:
    :return:
    """
    token = credentials.credentials
    return await repository.logout(refresh_token=token)


@user_router.get("/refresh_token", response_model=UserJwtToken)
async def refresh_user_token(
    repository: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> UserJwtToken:
    """
    Корутина рефрешит токен
    :param repository:
    :param credentials:
    :return:
    """
    token = credentials.credentials
    return await repository.refresh_token(refresh_token=token)


@user_router.get("/is_auth", response_model=UserJwtToken)
async def is_auth(
    repository: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> UserJwtToken:
    """
    Корутина проверяет логин
    :param repository:
    :param credentials:
    :return:
    """
    token = credentials.credentials
    return await repository.check_auth(refresh_token=token)
