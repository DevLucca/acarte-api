from . import BaseDTO
from pydantic.fields import Field
from datetime import datetime
from pydantic.class_validators import validator
from uuid import UUID

class Instrument(BaseDTO):
    id: int = None
    uuid: UUID = None
    name: str = None
    number: str = None
    itype: str = None
    notes: str = None
    repair: bool = None
    active: bool = None
    created_at: datetime = None
    updated_at: datetime = None

    class InstrumentPostSchema(BaseDTO):
        name: str = Field(...)
        number: str = Field(...)
        itype: str = Field(...)
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
        
        @validator("type")
        def validate_type(cls, val):
            assert val, 'type cannot be empty or missing'
            return val

    class InstrumentPutSchema(BaseDTO):
        notes: str = Field(None)
        repair: bool = Field(False)
        active: bool = Field(True)

    class InstrumentResponseSchema(BaseDTO):
        id: UUID = Field(...)
        name: str = Field(...)
        number: str = Field(...)
        itype: str = Field(...)
        notes: str = Field(None)
        repair: bool = Field(False)
        active: bool = Field(True)
