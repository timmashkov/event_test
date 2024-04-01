from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.employer.repository import (
    EmployerShowRepository,
    EmployerDataManagerRepository,
)
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
        self, repository: EmployerShowRepository = Depends(EmployerShowRepository)
    ):
        self.repository = repository

    async def get_all_employers(self) -> list[Employer]:
        answer = await self.repository.get_employers()
        return answer

    async def find_employer_by_id(self, cmd: GetEmployerById) -> EmployerReturn:
        answer = await self.repository.get_employer_by_id(cmd=cmd)
        if not answer:
            raise EmployerNotFound
        return answer

    async def find_employer_by_first(
        self, cmd: GetEmployerByFirstName
    ) -> EmployerReturn:
        answer = await self.repository.get_employer_by_first(cmd=cmd)
        if not answer:
            raise EmployerNotFound
        return answer

    async def find_employer_by_last(self, cmd: GetEmployerByLastName) -> EmployerReturn:
        answer = await self.repository.get_employer_by_last(cmd=cmd)
        if not answer:
            raise EmployerNotFound
        return answer


class EmployerDataManagerService:
    def __init__(
        self,
        repository: EmployerDataManagerRepository = Depends(
            EmployerDataManagerRepository
        ),
    ) -> None:
        self.repository = repository

    async def register_employer(self, cmd: RegisterEmployer) -> EmployerReturn:
        try:
            answer = await self.repository.create_employer(cmd=cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise EmployerAlreadyExist

    async def change_employer(
        self, cmd: UpdateEmployer, model_id: GetEmployerById
    ) -> EmployerReturn:
        answer = await self.repository.update_employer(cmd=cmd, model_id=model_id)
        if not answer:
            raise EmployerNotFound
        return answer

    async def drop_employer(self, model_id: GetEmployerById) -> EmployerReturn:
        answer = await self.repository.delete_employer(model_id=model_id)
        if not answer:
            raise EmployerNotFound
        return answer
