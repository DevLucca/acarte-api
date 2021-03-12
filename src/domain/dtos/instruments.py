from enum import Enum
from uuid import UUID
from datetime import datetime

from domain.dtos import BaseDTO
from domain.dtos.users import UserDTO

from pydantic.fields import Field
from pydantic.class_validators import validator

class InstrumentTypes(str, Enum):
    Wood = 'Madeira'
    Metal = 'Metal'
    String = 'Corda'
    Percussion = 'Percussão'
    Others = 'Outros'
    
class InstrumentDTO(BaseDTO):
    id: int = None
    uuid: UUID = None
    name: str = None
    number: str = None
    itype: InstrumentTypes = None
    notes: str = None
    repair: bool = None
    active: bool = None
    created_at: datetime = None
    updated_at: datetime = None
    updated_by: UserDTO = None

    class InstrumentPostSchema(BaseDTO):
        name: str = Field(...)
        number: str = Field(...)
        itype: InstrumentTypes = Field(...)
        notes: str = Field(None)
        repair: bool = Field(False)
        active: bool = Field(True)

        @validator("name")
        def validate_name(cls, val):
            assert val, 'name cannot be empty or missing'
            return val

        @validator("number")
        def validate_number(cls, val):
            assert val, 'number cannot be empty or missing'
            return val
        
        @validator("itype")
        def validate_itype(cls, val):
            assert val, 'itype cannot be empty or missing'
            return val

    class InstrumentPutSchema(BaseDTO):
        notes: str = Field(None)
        repair: bool = Field(False)
        active: bool = Field(True)

    class InstrumentResponseSchema(BaseDTO):
        uuid: UUID = Field(...)
        name: str = Field(...)
        number: str = Field(...)
        itype: InstrumentTypes = Field(...)
        notes: str = Field(None)
        repair: bool = Field(False)
        active: bool = Field(True)
        created_at: datetime = Field(...)
        updated_at: datetime = Field(None)
        updated_by: UserDTO.UserUpdatedByResponseSchema = Field(None)
