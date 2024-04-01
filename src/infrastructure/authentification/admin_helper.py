from typing import Any

from domain.user.schema import UserJwtToken, UserLogin
from infrastructure.authentification.auth_handler import AuthHandler
from infrastructure.database.db_helpers import find_user, change_token, find_token
from infrastructure.exceptions.token_exceptions import Unauthorized
from infrastructure.exceptions.user_exceptions import UserNotFound, WrongPassword
from infrastructure.utils.str_helper import convert_to_uuid

"""
Вспомогательные фичи для админки, для игзбегания DI
"""

auth = AuthHandler()


async def verify_user(cmd: UserLogin) -> dict[str, str] | dict[str, Any]:
    """подтверждение юзера"""
    user = await find_user(data=cmd)
    if not user:
        raise UserNotFound
    if not await auth.verify_password(cmd.password, cmd.login, user.password):
        raise WrongPassword
    access_token = await auth.encode_token(user.id)
    refresh_token = await auth.encode_refresh_token(user.id)
    try:
        await change_token(data=UserJwtToken(id=user.id, token=refresh_token))
    except Exception as e:
        return {"error": e}
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens


async def check_auth(refresh_token) -> UserJwtToken:
    """Подтверджение аутентификации"""
    user_id = await auth.decode_token(refresh_token)
    exist_token = await find_token(cmd=await convert_to_uuid(user_id))
    if not exist_token:
        raise Unauthorized
    try:
        if exist_token == refresh_token:
            return UserJwtToken(id=user_id, token=exist_token)
        else:
            raise Unauthorized
    except AttributeError:
        raise Unauthorized
