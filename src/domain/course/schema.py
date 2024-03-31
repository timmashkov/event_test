from uuid import UUID

from pydantic import BaseModel, field_validator, model_validator


class GetCourseById(BaseModel):
    id: UUID


class GetCourseByTitle(BaseModel):
    title: str


class CourseUpdate(GetCourseByTitle):
    price: int
    description: str
    duration: int


class CourseCreate(CourseUpdate):
    company_id: UUID


class CourseReturn(GetCourseById, CourseCreate):
    pass
