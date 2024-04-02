from uuid import UUID

from fastapi import APIRouter, Depends, status

from domain.teacher.schema import (
    GetTeacherById,
    TeacherReturn,
    GetTeacherByFirstName,
    GetTeacherByLastName,
    RegisterTeacher,
    UpdateTeacher,
)
from infrastructure.database.models import Teacher
from service.teacher_service import TeacherShowService, TeacherDataManagerService

teach_router = APIRouter(prefix="/teachers")


@teach_router.get("/all", response_model=list[TeacherReturn])
async def show_all_teach(
    repository: TeacherShowService = Depends(TeacherShowService),
) -> list[Teacher]:
    """
    Корутина возвращает список преподавателей
    :param repository:
    :return:
    """
    return await repository.get_all_teachers()


@teach_router.get("/search_id/{teach_id}", response_model=TeacherReturn)
async def show_teach_by_id(
    teach_id: UUID, repository: TeacherShowService = Depends(TeacherShowService)
) -> TeacherReturn:
    """
    Корутина возвращает препода по айди
    :param teach_id:
    :param repository:
    :return:
    """
    return await repository.find_teacher_by_id(cmd=GetTeacherById(id=teach_id))


@teach_router.get("/first_name/{first_name}", response_model=TeacherReturn)
async def show_teach_by_first(
    first_name: str, repository: TeacherShowService = Depends(TeacherShowService)
) -> TeacherReturn:
    """
    Корутина возвращает препода по имени
    :param first_name:
    :param repository:
    :return:
    """
    return await repository.find_teacher_by_first(
        cmd=GetTeacherByFirstName(first_name=first_name)
    )


@teach_router.get("/last_name/{last_name}", response_model=TeacherReturn)
async def show_teach_by_last(
    last_name: str, repository: TeacherShowService = Depends(TeacherShowService)
) -> TeacherReturn:
    """
    Корутина возвращает препода по фамилии
    :param last_name:
    :param repository:
    :return:
    """
    return await repository.find_teacher_by_last(
        cmd=GetTeacherByLastName(last_name=last_name)
    )


@teach_router.post(
    "/register_teach", response_model=TeacherReturn, status_code=status.HTTP_201_CREATED
)
async def registration_teach(
    cmd: RegisterTeacher,
    repository: TeacherDataManagerService = Depends(TeacherDataManagerService),
) -> TeacherReturn:
    """
    Корутина создает препода
    :param cmd:
    :param repository:
    :return:
    """
    return await repository.register_teacher(cmd=cmd)


@teach_router.patch("/upd/{teach_id}", response_model=TeacherReturn)
async def upd_teach(
    teach_id: UUID,
    cmd: UpdateTeacher,
    repository: TeacherDataManagerService = Depends(TeacherDataManagerService),
) -> TeacherReturn:
    """
    Корутина апдейтит препода
    :param teach_id:
    :param cmd:
    :param repository:
    :return:
    """
    return await repository.change_teacher(
        cmd=cmd, model_id=GetTeacherById(id=teach_id)
    )


@teach_router.delete("/del/{teach_id}", response_model=TeacherReturn)
async def del_teach(
    teach_id: UUID,
    repository: TeacherDataManagerService = Depends(TeacherDataManagerService),
) -> TeacherReturn:
    """
    Корутина удаляет препода
    :param teach_id:
    :param repository:
    :return:
    """
    return await repository.drop_teacher(model_id=GetTeacherById(id=teach_id))
