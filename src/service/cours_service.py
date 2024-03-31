from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.course.repository import (
    CourseShowRepository,
    CourseDataManagerRepository,
)
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
        self, repository: CourseShowRepository = Depends(CourseShowRepository)
    ):
        self.repository = repository

    async def get_all_courses(self) -> list[Course]:
        answer = await self.repository.get_courses()
        return answer

    async def find_course_by_id(self, cmd: GetCourseById) -> CourseReturn:
        answer = await self.repository.get_course_by_id(cmd=cmd)
        if not answer:
            raise CourseNotFound
        return answer

    async def find_course_by_name(self, cmd: GetCourseByTitle) -> CourseReturn:
        answer = await self.repository.get_course_by_title(cmd=cmd)
        if not answer:
            raise CourseNotFound
        return answer


class CompanyDataManagerService:
    def __init__(
        self,
        repository: CourseDataManagerRepository = Depends(CourseDataManagerRepository),
    ) -> None:
        self.repository = repository

    async def register_course(self, cmd: CourseCreate) -> CourseReturn:
        try:
            answer = await self.repository.create_course(cmd=cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise CourseAlreadyExist

    async def change_course(
        self, cmd: CourseUpdate, model_id: GetCourseById
    ) -> CourseReturn:
        answer = await self.repository.update_course(cmd=cmd, model_id=model_id)
        if not answer:
            raise CourseNotFound
        return answer

    async def drop_course(self, model_id: GetCourseById) -> CourseReturn:
        answer = await self.repository.delete_course(model_id=model_id)
        if not answer:
            raise CourseNotFound
        return answer
