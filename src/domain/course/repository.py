from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.course.schema import (
    GetCourseById,
    GetCourseByTitle,
    CourseReturn,
    CourseCreate,
    CourseUpdate,
    CourseWithTeachers,
)
from infrastructure.database.models import Course
from infrastructure.database.session import vortex


class CourseShowRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Course

    async def get_courses(self) -> list[Course]:
        stmt = select(self.model).order_by(self.model.price)
        answer = await self.session.execute(stmt)
        result = list(answer.scalars().all())
        return result

    async def get_course_by_id(self, cmd: GetCourseById) -> CourseReturn | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_course_by_title(self, cmd: GetCourseByTitle) -> CourseReturn | None:
        stmt = select(self.model).where(self.model.title == cmd.title)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_course_with_teachers(
        self, cmd: GetCourseById
    ) -> CourseWithTeachers | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.teachers))
            .where(self.model.id == cmd.id)
        )
        answer = await self.session.execute(stmt)
        result = answer.unique().scalar_one_or_none()
        return result


class CourseDataManagerRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Course

    async def create_course(self, cmd: CourseCreate) -> CourseReturn | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.title,
                self.model.price,
                self.model.description,
                self.model.duration,
                self.model.company_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_course(
        self, cmd: CourseUpdate, model_id: GetCourseById
    ) -> CourseReturn | None:
        stmt = (
            update(self.model)
            .where(self.model.id == model_id.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.title,
                self.model.price,
                self.model.description,
                self.model.duration,
                self.model.company_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_course(self, model_id: GetCourseById) -> CourseReturn | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == model_id.id)
            .returning(
                self.model.id,
                self.model.title,
                self.model.price,
                self.model.description,
                self.model.duration,
                self.model.company_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
