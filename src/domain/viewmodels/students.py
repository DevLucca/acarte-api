from pydantic.fields import Field
from domain.viewmodels import (
    BaseValidator,
    BaseModel
)

class RegisterStudentSchema(BaseValidator):
    name: str = Field(...)
    surname: str = Field(...)
    ra: int = Field(...)

class ResponseStudentSchema(BaseModel):
    uuid: str
    name: str
    surname: str
    ra: str
