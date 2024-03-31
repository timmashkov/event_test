from uuid import UUID

from pydantic import BaseModel, field_validator


class GetTeacherById(BaseModel):
    id: UUID


class GetTeacherByFirstName(BaseModel):
    first_name: str


class GetTeacherByLastName(BaseModel):
    last_name: str


class UpdateTeacher(GetTeacherByFirstName, GetTeacherByLastName):
    middle_name: str
    degree: str
    exp: int


class RegisterTeacher(UpdateTeacher):
    user_id: UUID


class TeacherReturn(GetTeacherById, RegisterTeacher):
    @field_validator("exp")
    def convert_exp(cls, data):
        return f"{data} years"
