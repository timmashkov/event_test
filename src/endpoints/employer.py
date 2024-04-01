from uuid import UUID

from fastapi import APIRouter, Depends, status

from domain.employer.schema import (
    GetEmployerById,
    EmployerReturn,
    GetEmployerByFirstName,
    GetEmployerByLastName,
    RegisterEmployer,
    UpdateEmployer,
)
from infrastructure.database.models import Employer
from service.emp_service import EmployerShowService, EmployerDataManagerService

emp_router = APIRouter(prefix="/employers")


@emp_router.get("/all", response_model=list[EmployerReturn])
async def show_all_emp(
    repository: EmployerShowService = Depends(EmployerShowService),
) -> list[Employer]:
    return await repository.get_all_employers()


@emp_router.get("/search_id/{emp_id}", response_model=EmployerReturn)
async def show_emp_by_id(
    emp_id: UUID, repository: EmployerShowService = Depends(EmployerShowService)
) -> EmployerReturn:
    return await repository.find_employer_by_id(cmd=GetEmployerById(id=emp_id))


@emp_router.get("/first_name/{first_name}", response_model=EmployerReturn)
async def show_teach_by_first(
    first_name: str, repository: EmployerShowService = Depends(EmployerShowService)
) -> EmployerReturn:
    return await repository.find_employer_by_first(
        cmd=GetEmployerByFirstName(first_name=first_name)
    )


@emp_router.get("/last_name/{last_name}", response_model=EmployerReturn)
async def show_teach_by_last(
    last_name: str, repository: EmployerShowService = Depends(EmployerShowService)
) -> EmployerReturn:
    return await repository.find_employer_by_last(
        cmd=GetEmployerByLastName(last_name=last_name)
    )


@emp_router.post(
    "/register_teach",
    response_model=EmployerReturn,
    status_code=status.HTTP_201_CREATED,
)
async def registration_emp(
    cmd: RegisterEmployer,
    repository: EmployerDataManagerService = Depends(EmployerDataManagerService),
) -> EmployerReturn:
    return await repository.register_employer(cmd=cmd)


@emp_router.patch("/upd/{emp_id}", response_model=EmployerReturn)
async def upd_teach(
    emp_id: UUID,
    cmd: UpdateEmployer,
    repository: EmployerDataManagerService = Depends(EmployerDataManagerService),
) -> EmployerReturn:
    return await repository.change_employer(
        cmd=cmd, model_id=GetEmployerById(id=emp_id)
    )


@emp_router.delete("/del/{emp_id}", response_model=EmployerReturn)
async def del_teach(
    emp_id: UUID,
    repository: EmployerDataManagerService = Depends(EmployerDataManagerService),
) -> EmployerReturn:
    return await repository.drop_employer(model_id=GetEmployerById(id=emp_id))
