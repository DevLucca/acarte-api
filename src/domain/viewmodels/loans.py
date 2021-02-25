from data.repositories import instruments
from pydantic.fields import Field
from domain.viewmodels import (
    BaseValidator,
    instruments,
    students
)
from typing import List

class RegisterLoanSchema(BaseValidator):
    instrument_uuid: str = Field(...)
    student_uuid: str = Field(...)

class ResponseLoanSchema(BaseValidator):
    uuid: str
    instrument: List[instruments.ResponseInstrumentSchema]
    student: students.ResponseStudentSchema
    lented_at: str
    returned_at: str
