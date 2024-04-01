from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.teacher.repository import (
    TeacherShowRepository,
    TeacherDataManagerRepository,
)
from infrastructure.cache.cache_handler import CacheService
from infrastructure.database.models import Teacher
from domain.teacher.schema import (
    GetTeacherById,
    TeacherReturn,
    GetTeacherByFirstName,
    GetTeacherByLastName,
    RegisterTeacher,
    UpdateTeacher,
)
from infrastructure.exceptions.teacher_exceptions import (
    TeacherNotFound,
    TeacherAlreadyExist,
)


class TeacherShowService:
    def __init__(
        self,
        repository: TeacherShowRepository = Depends(TeacherShowRepository),
        cacher: CacheService = Depends(CacheService),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_teachers(self) -> list[Teacher]:
        answer = await self.repository.get_teachers()
        await self.cacher.read_cache(self._key)
        return answer

    async def find_teacher_by_id(self, cmd: GetTeacherById) -> TeacherReturn:
        answer = await self.repository.get_teacher_by_id(cmd=cmd)
        if not answer:
            raise TeacherNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_teacher_by_first(self, cmd: GetTeacherByFirstName) -> TeacherReturn:
        answer = await self.repository.get_teacher_by_first(cmd=cmd)
        if not answer:
            raise TeacherNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_teacher_by_last(self, cmd: GetTeacherByLastName) -> TeacherReturn:
        answer = await self.repository.get_teacher_by_last(cmd=cmd)
        if not answer:
            raise TeacherNotFound
        await self.cacher.read_cache(self._key)
        return answer


class TeacherDataManagerService:
    def __init__(
        self,
        repository: TeacherDataManagerRepository = Depends(
            TeacherDataManagerRepository
        ),
        cacher: CacheService = Depends(CacheService),
    ) -> None:
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def register_teacher(self, cmd: RegisterTeacher) -> TeacherReturn:
        try:
            answer = await self.repository.create_teacher(cmd=cmd)
            await self.cacher.create_cache(self._key, cmd.model_dump())
            return answer
        except (UniqueViolationError, IntegrityError):
            raise TeacherAlreadyExist

    async def change_teacher(
        self, cmd: UpdateTeacher, model_id: GetTeacherById
    ) -> TeacherReturn:
        answer = await self.repository.update_teacher(cmd=cmd, model_id=model_id)
        if not answer:
            raise TeacherNotFound
        await self.cacher.create_cache(self._key, cmd.model_dump())
        return answer

    async def drop_teacher(self, model_id: GetTeacherById) -> TeacherReturn:
        answer = await self.repository.delete_teacher(model_id=model_id)
        if not answer:
            raise TeacherNotFound
        await self.cacher.delete_cache(self._key)
        return answer
