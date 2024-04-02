from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.company.schema import (
    GetCompanyById,
    GetCompanyByName,
    CompanyReturn,
    CompanyCreate,
    CompanyWithCommand,
    CompanyWithCourse,
    CompanyFull,
)
from infrastructure.database.models import Company
from infrastructure.database.session import vortex


class CompanyShowRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Company

    async def get_comps(self) -> list[Company]:
        stmt = select(self.model).order_by(self.model.name)
        answer = await self.session.execute(stmt)
        result = list(answer.scalars().all())
        return result

    async def get_comp_by_id(self, cmd: GetCompanyById) -> CompanyReturn | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_comp_by_name(self, cmd: GetCompanyByName) -> CompanyReturn | None:
        stmt = select(self.model).where(self.model.name == cmd.name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_comp_with_emps(
        self, cmd: GetCompanyById
    ) -> CompanyWithCommand | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.command))
            .where(self.model.id == cmd.id)
        )
        answer = await self.session.execute(stmt)
        result = answer.unique().scalar_one_or_none()
        return result

    async def get_comp_with_cours(
        self, cmd: GetCompanyById
    ) -> CompanyWithCourse | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.courses))
            .where(self.model.id == cmd.id)
        )
        answer = await self.session.execute(stmt)
        result = answer.unique().scalar_one_or_none()
        return result

    async def get_comp_full(self, cmd: GetCompanyById) -> CompanyFull | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.command))
            .options(joinedload(self.model.courses))
            .where(self.model.id == cmd.id)
        )
        answer = await self.session.execute(stmt)
        result = answer.unique().scalar_one_or_none()
        return result


class CompanyDataManagerRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_scope)):
        self.session = session
        self.model = Company

    async def create_comp(self, cmd: CompanyCreate) -> CompanyReturn | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.name,
                self.model.email,
                self.model.bio,
                self.model.phone_number,
                self.model.address,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_comp(
        self, cmd: CompanyCreate, model_id: GetCompanyById
    ) -> CompanyReturn | None:
        stmt = (
            update(self.model)
            .where(self.model.id == model_id.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.name,
                self.model.email,
                self.model.bio,
                self.model.phone_number,
                self.model.address,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_comp(self, model_id: GetCompanyById) -> CompanyReturn | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == model_id.id)
            .returning(
                self.model.id,
                self.model.name,
                self.model.email,
                self.model.bio,
                self.model.phone_number,
                self.model.address,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
