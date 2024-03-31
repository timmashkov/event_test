from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.teacher.schema import (
    GetTeacherById,
    TeacherReturn,
    GetTeacherByFirstName,
    GetTeacherByLastName,
    RegisterTeacher,
    UpdateTeacher,
)
from infrastructure.database.models import Teacher
from infrastructure.database.session import vortex


class TeacherShowRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Teacher

    async def get_teachers(self) -> list[Teacher]:
        stmt = select(self.model).order_by(self.model.degree)
        answer = await self.session.execute(stmt)
        result = list(answer.scalars().all())
        return result

    async def get_teacher_by_id(self, cmd: GetTeacherById) -> TeacherReturn | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_teacher_by_first(
        self, cmd: GetTeacherByFirstName
    ) -> TeacherReturn | None:
        stmt = select(self.model).where(self.model.first_name == cmd.first_name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_teacher_by_last(
        self, cmd: GetTeacherByLastName
    ) -> TeacherReturn | None:
        stmt = select(self.model).where(self.model.last_name == cmd.last_name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result


class TeacherDataManagerRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Teacher

    async def create_teacher(self, cmd: RegisterTeacher) -> TeacherReturn | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.user_id,
                self.model.first_name,
                self.model.last_name,
                self.model.middle_name,
                self.model.degree,
                self.model.exp,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_teacher(
        self, cmd: UpdateTeacher, model_id: GetTeacherById
    ) -> TeacherReturn | None:
        stmt = (
            update(self.model)
            .where(self.model.id == model_id.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.user_id,
                self.model.first_name,
                self.model.last_name,
                self.model.middle_name,
                self.model.degree,
                self.model.exp,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_teacher(self, model_id: GetTeacherById) -> TeacherReturn | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == model_id.id)
            .returning(
                self.model.id,
                self.model.id,
                self.model.user_id,
                self.model.first_name,
                self.model.last_name,
                self.model.middle_name,
                self.model.degree,
                self.model.exp,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
