from uuid import UUID

from pydantic import BaseModel, field_validator


class GetEmployerById(BaseModel):
    id: UUID


class GetEmployerByFirstName(BaseModel):
    first_name: str


class GetEmployerByLastName(BaseModel):
    last_name: str


class UpdateEmployer(GetEmployerByFirstName, GetEmployerByLastName):
    middle_name: str
    position: str
    exp: int
    bio: str


class RegisterEmployer(UpdateEmployer):
    user_id: UUID
    company_id: UUID


class EmployerReturn(GetEmployerById, RegisterEmployer):
    @field_validator("exp")
    def convert_exp(cls, data):
        return f"{data} years"
