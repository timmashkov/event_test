from uuid import UUID

from pydantic import BaseModel, field_validator


class GetCourseById(BaseModel):
    id: UUID


class GetCourseByTitle(BaseModel):
    title: str


class CourseUpdate(GetCourseByTitle):
    price: int
    description: str
    duration: int

    @field_validator("duration")
    def convert_exp(cls, data):
        return f"{data} days"


class CourseCreate(CourseUpdate):
    company_id: UUID


class CourseReturn(GetCourseById, CourseCreate):
    pass
