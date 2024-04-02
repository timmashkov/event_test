from uuid import UUID

from fastapi import APIRouter, Depends, status

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
from service.company_service import CompanyShowService, CompanyDataManagerService

comp_router = APIRouter(prefix="/company")


@comp_router.get("/all", response_model=list[CompanyReturn])
async def show_all_comp(
    repository: CompanyShowService = Depends(CompanyShowService),
) -> list[Company]:
    """
    Корутина возвращает список компаний
    :param repository:
    :return:
    """
    return await repository.get_all_comps()


@comp_router.get("/search_id/{comp_id}", response_model=CompanyReturn)
async def show_comp_by_id(
    comp_id: UUID, repository: CompanyShowService = Depends(CompanyShowService)
) -> CompanyReturn:
    """
    Корутина возвращает компанию по айди
    :param comp_id:
    :param repository:
    :return:
    """
    return await repository.find_comps_by_id(cmd=GetCompanyById(id=comp_id))


@comp_router.get("/emps/{comp_id}", response_model=CompanyWithCommand)
async def show_comp_emps(
    comp_id: UUID, repository: CompanyShowService = Depends(CompanyShowService)
) -> CompanyWithCommand:
    """
    Корутина возвращает компанию со списком сотрудников
    :param comp_id:
    :param repository:
    :return:
    """
    return await repository.show_comp_with_emps(cmd=GetCompanyById(id=comp_id))


@comp_router.get("/courses/{comp_id}", response_model=CompanyWithCourse)
async def show_comp_cours(
    comp_id: UUID, repository: CompanyShowService = Depends(CompanyShowService)
) -> CompanyWithCourse:
    """
    Корутина возвращает компанию со списком курсов
    :param comp_id:
    :param repository:
    :return:
    """
    return await repository.show_comp_with_cours(cmd=GetCompanyById(id=comp_id))


@comp_router.get("/full/{comp_id}", response_model=CompanyFull)
async def show_comp_full(
    comp_id: UUID, repository: CompanyShowService = Depends(CompanyShowService)
) -> CompanyFull:
    """
    Корутина возвращает компанию со списком курсов и списком сотрудников
    :param comp_id:
    :param repository:
    :return:
    """
    return await repository.show_comp_full(cmd=GetCompanyById(id=comp_id))


@comp_router.get("/search_name/{name}", response_model=CompanyReturn)
async def show_comp_by_name(
    name: str, repository: CompanyShowService = Depends(CompanyShowService)
) -> CompanyReturn:
    """
    Корутина возвращает компанию по названию
    :param name:
    :param repository:
    :return:
    """
    return await repository.find_comps_by_name(cmd=GetCompanyByName(name=name))


@comp_router.post(
    "/register_comp", response_model=CompanyReturn, status_code=status.HTTP_201_CREATED
)
async def registration_comp(
    cmd: CompanyCreate,
    repository: CompanyDataManagerService = Depends(CompanyDataManagerService),
) -> CompanyReturn:
    """
    Корутина для создания компании
    :param cmd:
    :param repository:
    :return:
    """
    return await repository.register_comp(cmd=cmd)


@comp_router.patch("/upd/{comp_id}", response_model=CompanyReturn)
async def upd_comp(
    comp_id: UUID,
    cmd: CompanyCreate,
    repository: CompanyDataManagerService = Depends(CompanyDataManagerService),
) -> CompanyReturn:
    """
    Корутина апдейтит компанию
    :param comp_id:
    :param cmd:
    :param repository:
    :return:
    """
    return await repository.change_comp(cmd=cmd, model_id=GetCompanyById(id=comp_id))


@comp_router.delete("/del/{comp_id}", response_model=CompanyReturn)
async def del_comp(
    comp_id: UUID,
    repository: CompanyDataManagerService = Depends(CompanyDataManagerService),
) -> CompanyReturn:
    """
    Корутина удаляет компанию
    :param comp_id:
    :param repository:
    :return:
    """
    return await repository.drop_comp(model_id=GetCompanyById(id=comp_id))
