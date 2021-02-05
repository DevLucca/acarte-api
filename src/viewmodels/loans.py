from repository import instruments
from pydantic.fields import Field
from viewmodels import (
    BaseValidator,
    BaseModel,
    instruments,
    students
)

class RegisterLoanSchema(BaseValidator):
    instrument_uuid: str = Field(...)
    student_uuid: str = Field(...)

class ResponseLoanSchema(BaseModel):
    uuid: str
    instrument: instruments.ResponseInstrumentSchema
    student: students.ResponseStudentSchema
    lented_at: str
    returned_at: str
