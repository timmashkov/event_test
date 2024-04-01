from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.course.repository import (
    CourseShowRepository,
    CourseDataManagerRepository,
)
from infrastructure.cache.cache_handler import CacheService
from infrastructure.database.models import Course
from domain.course.schema import (
    GetCourseById,
    GetCourseByTitle,
    CourseReturn,
    CourseCreate,
    CourseUpdate,
)
from infrastructure.exceptions.cours_exception import (
    CourseNotFound,
    CourseAlreadyExist,
)


class CompanyShowService:
    def __init__(
        self,
        repository: CourseShowRepository = Depends(CourseShowRepository),
        cacher: CacheService = Depends(CacheService),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_courses(self) -> list[Course]:
        answer = await self.repository.get_courses()
        await self.cacher.read_cache(self._key)
        return answer

    async def find_course_by_id(self, cmd: GetCourseById) -> CourseReturn:
        answer = await self.repository.get_course_by_id(cmd=cmd)
        if not answer:
            raise CourseNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_course_by_name(self, cmd: GetCourseByTitle) -> CourseReturn:
        answer = await self.repository.get_course_by_title(cmd=cmd)
        if not answer:
            raise CourseNotFound
        await self.cacher.read_cache(self._key)
        return answer


class CompanyDataManagerService:
    def __init__(
        self,
        repository: CourseDataManagerRepository = Depends(CourseDataManagerRepository),
        cacher: CacheService = Depends(CacheService),
    ) -> None:
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def register_course(self, cmd: CourseCreate) -> CourseReturn:
        try:
            answer = await self.repository.create_course(cmd=cmd)
            await self.cacher.create_cache(self._key, cmd.model_dump())
            return answer
        except (UniqueViolationError, IntegrityError):
            raise CourseAlreadyExist

    async def change_course(
        self, cmd: CourseUpdate, model_id: GetCourseById
    ) -> CourseReturn:
        answer = await self.repository.update_course(cmd=cmd, model_id=model_id)
        if not answer:
            raise CourseNotFound
        await self.cacher.create_cache(self._key, cmd.model_dump())
        return answer

    async def drop_course(self, model_id: GetCourseById) -> CourseReturn:
        answer = await self.repository.delete_course(model_id=model_id)
        if not answer:
            raise CourseNotFound
        await self.cacher.delete_cache(self._key)
        return answer
