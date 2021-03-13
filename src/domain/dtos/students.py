from uuid import UUID
from datetime import datetime
from domain.dtos import BaseDTO
from pydantic.fields import Field
from domain.dtos.users import UserDTO
from pydantic.class_validators import validator
    
class StudentDTO(BaseDTO):
    id: int = None
    uuid: UUID = None
    name: str = None
    surname: str = None
    ra: str = None
    blocked: bool = None
    active: bool = None
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: UserDTO = None

    class StudentPostSchema(BaseDTO):
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

    class StudentPutSchema(BaseDTO):
        name: str = Field(...)
        surname: str = Field(...)
        blocked: bool = Field(False)
        active: bool = Field(True)

    class StudentResponseSchema(BaseDTO):
        uuid: UUID = Field(...)
        name: str = Field(...)
        surname: str = Field(...)
        ra: str = Field(None)
        blocked: bool = Field(False)
        active: bool = Field(True)
        created_at: datetime = Field(...)
        updated_at: datetime = Field(None)
        updated_by: UserDTO.UserUpdatedByResponseSchema = Field(None)
        
    class StudentLoanResponseSchema(BaseDTO):
        uuid: UUID = Field(...)
        name: str = Field(...)
        surname: str = Field(...)
        ra: str = Field(None)
