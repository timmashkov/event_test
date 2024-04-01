from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.user.repository import UserShowRepository, UserDataManagerRepository
from domain.user.schema import (
    UserReturnData,
    GetUserById,
    GetUserByLogin,
    CreateUser,
    UpdateUser,
)
from infrastructure.authentification.auth_handler import AuthHandler
from infrastructure.cache.cache_handler import CacheService
from infrastructure.database.models import User
from infrastructure.exceptions.user_exceptions import UserNotFound, UserAlreadyExist


class UserShowService:
    def __init__(
        self,
        repository: UserShowRepository = Depends(UserShowRepository),
        cacher: CacheService = Depends(CacheService),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_users(self) -> list[User]:
        answer = await self.repository.get_users()
        await self.cacher.read_cache(self._key)
        return answer

    async def find_user_by_id(self, cmd: GetUserById) -> UserReturnData:
        answer = await self.repository.get_user_by_id(cmd=cmd)
        if not answer:
            raise UserNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_user_by_login(self, cmd: GetUserByLogin) -> UserReturnData:
        answer = await self.repository.get_user_by_login(cmd=cmd)
        if not answer:
            raise UserNotFound
        await self.cacher.read_cache(self._key)
        return answer


class UserDataManagerService:
    def __init__(
        self,
        repository: UserDataManagerRepository = Depends(UserDataManagerRepository),
        auth: AuthHandler = Depends(AuthHandler),
        cacher: CacheService = Depends(CacheService),
    ) -> None:
        self.repository = repository
        self.auth = auth
        self.cacher = cacher
        self._key = str(self.__class__)

    async def register_user(self, cmd: CreateUser) -> UserReturnData:
        try:
            salted_pass = await self.auth.encode_pass(cmd.password, cmd.login)
            data = CreateUser(
                login=cmd.login,
                password=salted_pass,
                email=cmd.email,
                phone_number=cmd.phone_number,
                age=cmd.age,
            )
            answer = await self.repository.create_user(cmd=data)
            await self.cacher.create_cache(self._key, data.model_dump())
            return answer
        except (UniqueViolationError, IntegrityError):
            raise UserAlreadyExist

    async def change_user(
        self, cmd: UpdateUser, model_id: GetUserById
    ) -> UserReturnData:
        answer = await self.repository.update_user(cmd=cmd, model_id=model_id)
        if not answer:
            raise UserNotFound
        await self.cacher.create_cache(self._key, cmd.model_dump())
        return answer

    async def drop_user(self, model_id: GetUserById) -> UserReturnData:
        answer = await self.repository.delete_user(model_id=model_id)
        if not answer:
            raise UserNotFound
        await self.cacher.delete_cache(self._key)
        return answer
