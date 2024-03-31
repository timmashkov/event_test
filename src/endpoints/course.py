from uuid import UUID

from fastapi import APIRouter, Depends, status

from domain.course.schema import (
    GetCourseById,
    GetCourseByTitle,
    CourseReturn,
    CourseCreate,
    CourseUpdate,
)
from infrastructure.database.models import Course
from service.cours_service import CompanyShowService, CompanyDataManagerService

cour_router = APIRouter(prefix="/courses")


@cour_router.get("/all", response_model=list[CourseReturn])
async def show_all_courses(
    repository: CompanyShowService = Depends(CompanyShowService),
) -> list[Course]:
    return await repository.get_all_courses()


@cour_router.get("/search_id/{cour_id}", response_model=CourseReturn)
async def show_course_by_id(
    cour_id: UUID, repository: CompanyShowService = Depends(CompanyShowService)
) -> CourseReturn:
    return await repository.find_course_by_id(cmd=GetCourseById(id=cour_id))


@cour_router.get("/search_title/{title}", response_model=CourseReturn)
async def show_course_by_name(
    title: str, repository: CompanyShowService = Depends(CompanyShowService)
) -> CourseReturn:
    return await repository.find_course_by_name(cmd=GetCourseByTitle(title=title))


@cour_router.post(
    "/register_comp", response_model=CourseReturn, status_code=status.HTTP_201_CREATED
)
async def registration_course(
    cmd: CourseCreate,
    repository: CompanyDataManagerService = Depends(CompanyDataManagerService),
) -> CourseReturn:
    return await repository.register_course(cmd=cmd)


@cour_router.patch("/upd/{cour_id}", response_model=CourseReturn)
async def upd_course(
    cour_id: UUID,
    cmd: CourseUpdate,
    repository: CompanyDataManagerService = Depends(CompanyDataManagerService),
) -> CourseReturn:
    return await repository.change_course(cmd=cmd, model_id=GetCourseById(id=cour_id))


@cour_router.delete("/del/{cour_id}", response_model=CourseReturn)
async def del_course(
    cour_id: UUID,
    repository: CompanyDataManagerService = Depends(CompanyDataManagerService),
) -> CourseReturn:
    return await repository.drop_course(model_id=GetCourseById(id=cour_id))
