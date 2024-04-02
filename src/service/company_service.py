from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.company.repository import (
    CompanyShowRepository,
    CompanyDataManagerRepository,
)
from infrastructure.cache.cache_handler import CacheService
from infrastructure.database.models import Company
from domain.company.schema import (
    GetCompanyById,
    GetCompanyByName,
    CompanyReturn,
    CompanyCreate,
    CompanyWithCommand,
    CompanyWithCourse,
    CompanyFull,
)
from infrastructure.exceptions.comp_exceptions import (
    CompanyNotFound,
    CompanyAlreadyExist,
)


class CompanyShowService:
    def __init__(
        self,
        repository: CompanyShowRepository = Depends(CompanyShowRepository),
        cacher: CacheService = Depends(CacheService),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_comps(self) -> list[Company]:
        await self.cacher.read_cache(self._key)
        answer = await self.repository.get_comps()
        return answer

    async def find_comps_by_id(self, cmd: GetCompanyById) -> CompanyReturn:
        answer = await self.repository.get_comp_by_id(cmd=cmd)
        if not answer:
            raise CompanyNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_comps_by_name(self, cmd: GetCompanyByName) -> CompanyReturn:
        answer = await self.repository.get_comp_by_name(cmd=cmd)
        if not answer:
            raise CompanyNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def show_comp_with_emps(self, cmd: GetCompanyById) -> CompanyWithCommand:
        answer = await self.repository.get_comp_with_emps(cmd=cmd)
        if not answer:
            raise CompanyNotFound
        return answer

    async def show_comp_with_cours(self, cmd: GetCompanyById) -> CompanyWithCourse:
        answer = await self.repository.get_comp_with_cours(cmd=cmd)
        if not answer:
            raise CompanyNotFound
        return answer

    async def show_comp_full(self, cmd: GetCompanyById) -> CompanyFull:
        answer = await self.repository.get_comp_full(cmd=cmd)
        if not answer:
            raise CompanyNotFound
        return answer


class CompanyDataManagerService:
    def __init__(
        self,
        repository: CompanyDataManagerRepository = Depends(
            CompanyDataManagerRepository
        ),
        cacher: CacheService = Depends(CacheService),
    ) -> None:
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def register_comp(self, cmd: CompanyCreate) -> CompanyReturn:
        try:
            answer = await self.repository.create_comp(cmd=cmd)
            await self.cacher.create_cache(self._key, cmd.model_dump())
            return answer
        except (UniqueViolationError, IntegrityError):
            raise CompanyAlreadyExist

    async def change_comp(
        self, cmd: CompanyCreate, model_id: GetCompanyById
    ) -> CompanyReturn:
        answer = await self.repository.update_comp(cmd=cmd, model_id=model_id)
        if not answer:
            raise CompanyNotFound
        await self.cacher.create_cache(self._key, cmd.model_dump())
        return answer

    async def drop_comp(self, model_id: GetCompanyById) -> CompanyReturn:
        answer = await self.repository.delete_comp(model_id=model_id)
        if not answer:
            raise CompanyNotFound
        await self.cacher.delete_cache(self._key)
        return answer
