from uuid import UUID
from typing import List
from datetime import datetime

from domain.dtos import BaseDTO
from domain.dtos.users import UserDTO
from domain.dtos.students import StudentDTO
from domain.dtos.instruments import InstrumentDTO

from pydantic.fields import Field
from pydantic.class_validators import validator
    
class LoanDTO(BaseDTO):
    id: int = None
    uuid: UUID = None
    instruments: List[InstrumentDTO] = None
    student: StudentDTO = None
    lented_at: datetime = None
    returned_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: UserDTO = None

    class LoanPostSchema(BaseDTO):
        instruments: List[UUID] = Field(...)
        student: UUID = Field(...)

        @validator("instruments")
        def validate_instruments(cls, val):
            assert val, 'name cannot be empty or missing'
            return val

        @validator("student")
        def validate_student(cls, val):
            assert val, 'number cannot be empty or missing'
            return val

    class LoanPutSchema(BaseDTO):
        is_returned: bool = Field(False)

    class LoanResponseSchema(BaseDTO):
        uuid: UUID = Field(...)
        instruments: List[InstrumentDTO.InstrumentLoanResponseSchema] = Field(...)
        student: StudentDTO.StudentLoanResponseSchema = Field(...)
        lented_at: datetime = Field(...)
        returned_at: datetime = Field(None)
        created_at: datetime = Field(...)
        updated_at: datetime = Field(None)
        updated_by: UserDTO.UserUpdatedByResponseSchema = Field(None)
