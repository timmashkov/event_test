from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.company.repository import (
    CompanyShowRepository,
    CompanyDataManagerRepository,
)
from infrastructure.database.models import Company
from domain.company.schema import (
    GetCompanyById,
    GetCompanyByName,
    CompanyReturn,
    CompanyCreate,
)
from infrastructure.exceptions.comp_exceptions import (
    CompanyNotFound,
    CompanyAlreadyExist,
)


class CompanyShowService:
    def __init__(
        self, repository: CompanyShowRepository = Depends(CompanyShowRepository)
    ):
        self.repository = repository

    async def get_all_comps(self) -> list[Company]:
        answer = await self.repository.get_comps()
        return answer

    async def find_comps_by_id(self, cmd: GetCompanyById) -> CompanyReturn:
        answer = await self.repository.get_comp_by_id(cmd=cmd)
        if not answer:
            raise CompanyNotFound
        return answer

    async def find_comps_by_name(self, cmd: GetCompanyByName) -> CompanyReturn:
        answer = await self.repository.get_comp_by_name(cmd=cmd)
        if not answer:
            raise CompanyNotFound
        return answer


class CompanyDataManagerService:
    def __init__(
        self,
        repository: CompanyDataManagerRepository = Depends(
            CompanyDataManagerRepository
        ),
    ) -> None:
        self.repository = repository

    async def register_comp(self, cmd: CompanyCreate) -> CompanyReturn:
        try:
            answer = await self.repository.create_comp(cmd=cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise CompanyAlreadyExist

    async def change_comp(
        self, cmd: CompanyCreate, model_id: GetCompanyById
    ) -> CompanyReturn:
        answer = await self.repository.update_comp(cmd=cmd, model_id=model_id)
        if not answer:
            raise CompanyNotFound
        return answer

    async def drop_comp(self, model_id: GetCompanyById) -> CompanyReturn:
        answer = await self.repository.delete_comp(model_id=model_id)
        if not answer:
            raise CompanyNotFound
        return answer
