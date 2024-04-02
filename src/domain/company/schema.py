from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from domain.course.schema import CourseReturn
from domain.employer.schema import EmployerReturn


class GetCompanyById(BaseModel):
    id: UUID


class GetCompanyByName(BaseModel):
    name: str


class CompanyCreate(GetCompanyByName):
    email: EmailStr
    bio: str
    phone_number: str = Field(examples=["89986661488", "+79986661488"])
    address: str

    @field_validator("phone_number")
    def check_number(cls, value):
        if (value.isdigit() and len(value) == 11) or (
            value[1:].isdigit() and value.startswith("+") and len(value) == 12
        ):
            return value
        raise ValueError("Invalid phone number")


class CompanyReturn(GetCompanyById, CompanyCreate):
    pass


class CompanyWithCommand(CompanyReturn):
    command: list[EmployerReturn] | None


class CompanyWithCourse(CompanyReturn):
    courses: list[CourseReturn] | None


class CompanyFull(CompanyWithCommand, CompanyWithCourse):
    pass
