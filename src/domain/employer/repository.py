from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.employer.schema import (
    GetEmployerById,
    EmployerReturn,
    GetEmployerByFirstName,
    GetEmployerByLastName,
    RegisterEmployer,
    UpdateEmployer,
)
from infrastructure.database.models import Employer
from infrastructure.database.session import vortex


class EmployerShowRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Employer

    async def get_employers(self) -> list[Employer]:
        stmt = select(self.model).order_by(self.model.exp)
        answer = await self.session.execute(stmt)
        result = list(answer.scalars().all())
        return result

    async def get_employer_by_id(self, cmd: GetEmployerById) -> EmployerReturn | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_employer_by_first(
        self, cmd: GetEmployerByFirstName
    ) -> EmployerReturn | None:
        stmt = select(self.model).where(self.model.first_name == cmd.first_name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_employer_by_last(
        self, cmd: GetEmployerByLastName
    ) -> EmployerReturn | None:
        stmt = select(self.model).where(self.model.last_name == cmd.last_name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result


class EmployerDataManagerRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Employer

    async def create_employer(self, cmd: RegisterEmployer) -> EmployerReturn | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.user_id,
                self.model.first_name,
                self.model.last_name,
                self.model.middle_name,
                self.model.position,
                self.model.exp,
                self.model.company_id,
                self.model.bio,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_employer(
        self, cmd: UpdateEmployer, model_id: GetEmployerById
    ) -> EmployerReturn | None:
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
                self.model.position,
                self.model.exp,
                self.model.company_id,
                self.model.bio,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_employer(self, model_id: GetEmployerById) -> EmployerReturn | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == model_id.id)
            .returning(
                self.model.id,
                self.model.user_id,
                self.model.first_name,
                self.model.last_name,
                self.model.middle_name,
                self.model.position,
                self.model.exp,
                self.model.company_id,
                self.model.bio,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
