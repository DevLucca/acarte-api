from pydantic.fields import Field
from pydantic.class_validators import validator
from domain.viewmodels import (
    BaseValidator
)

class RegisterStudentSchema(BaseValidator):
    name: str = Field(...)
    surname: str = Field(...)
    ra: str = Field(...)
    blocked: bool = Field(False)
    active: bool = Field(True)

    @validator("name")
    def validate_name(cls, val):
        assert val, 'name cannot be empty or missing'
        return val

    @validator("surname")
    def validate_surname(cls, val):
        assert val, 'surname cannot be empty or missing'
        return val

    @validator("ra")
    def validate_ra(cls, val):
        assert val, 'ra cannot be empty or missing'
        return val

class ResponseStudentSchema(BaseValidator):
    uuid: str
    name: str
    surname: str
    ra: str
    blocked: bool
    active: bool
