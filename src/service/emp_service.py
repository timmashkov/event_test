from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.employer.repository import (
    EmployerShowRepository,
    EmployerDataManagerRepository,
)
from infrastructure.cache.cache_handler import CacheService
from infrastructure.database.models import Employer
from domain.employer.schema import (
    GetEmployerById,
    EmployerReturn,
    GetEmployerByFirstName,
    GetEmployerByLastName,
    RegisterEmployer,
    UpdateEmployer,
)
from infrastructure.exceptions.emp_exception import (
    EmployerNotFound,
    EmployerAlreadyExist,
)


class EmployerShowService:
    def __init__(
        self,
        repository: EmployerShowRepository = Depends(EmployerShowRepository),
        cacher: CacheService = Depends(CacheService),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_employers(self) -> list[Employer]:
        answer = await self.repository.get_employers()
        await self.cacher.read_cache(self._key)
        return answer

    async def find_employer_by_id(self, cmd: GetEmployerById) -> EmployerReturn:
        answer = await self.repository.get_employer_by_id(cmd=cmd)
        if not answer:
            raise EmployerNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_employer_by_first(
        self, cmd: GetEmployerByFirstName
    ) -> EmployerReturn:
        answer = await self.repository.get_employer_by_first(cmd=cmd)
        if not answer:
            raise EmployerNotFound
        await self.cacher.read_cache(self._key)
        return answer

    async def find_employer_by_last(self, cmd: GetEmployerByLastName) -> EmployerReturn:
        answer = await self.repository.get_employer_by_last(cmd=cmd)
        if not answer:
            raise EmployerNotFound
        await self.cacher.read_cache(self._key)
        return answer


class EmployerDataManagerService:
    def __init__(
        self,
        repository: EmployerDataManagerRepository = Depends(
            EmployerDataManagerRepository
        ),
        cacher: CacheService = Depends(CacheService),
    ) -> None:
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def register_employer(self, cmd: RegisterEmployer) -> EmployerReturn:
        try:
            answer = await self.repository.create_employer(cmd=cmd)
            await self.cacher.create_cache(self._key, cmd.model_dump())
            return answer
        except (UniqueViolationError, IntegrityError):
            raise EmployerAlreadyExist

    async def change_employer(
        self, cmd: UpdateEmployer, model_id: GetEmployerById
    ) -> EmployerReturn:
        answer = await self.repository.update_employer(cmd=cmd, model_id=model_id)
        if not answer:
            raise EmployerNotFound
        await self.cacher.create_cache(self._key, cmd.model_dump())
        return answer

    async def drop_employer(self, model_id: GetEmployerById) -> EmployerReturn:
        answer = await self.repository.delete_employer(model_id=model_id)
        if not answer:
            raise EmployerNotFound
        await self.cacher.delete_cache(self._key)
        return answer
