from pydantic.fields import Field
from pydantic.class_validators import validator
from domain.viewmodels import (
    BaseValidator
)

class RegisterInstrumentSchema(BaseValidator):
    name: str = Field(...)
    instrument_id: str = Field(...)
    instrument_type: str = Field(...)
    notes: str = Field(None)
    repair: bool = Field(False)
    active: bool = Field(True)

    @validator("name")
    def validate_name(cls, val):
        assert val, 'name cannot be empty or missing'
        return val

    @validator("instrument_id")
    def validate_instrument_id(cls, val):
        assert val, 'instrument_id cannot be empty or missing'
        return val
    
    @validator("instrument_type")
    def validate_instrument_type(cls, val):
        assert val, 'instrument_type cannot be empty or missing'
        return val
    
    @validator("notes")
    def validate_notes(cls, val):
        return val if val else ""

class ResponseInstrumentSchema(BaseValidator):
    uuid: str
    instrument_id: str
    name: str
    instrument_type: str
    notes: str
    repair: bool
    active: bool
