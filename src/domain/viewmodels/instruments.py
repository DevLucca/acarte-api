from pydantic.fields import Field
from domain.viewmodels import (
    BaseValidator,
    BaseModel
)

class RegisterInstrumentSchema(BaseValidator):
    name: str = Field(...)
    instrument_id: str = Field(...)
    instrument_type: str = Field(...)
    notes: str = Field(...)
    repair: bool = Field(False)
    active: bool = Field(True)

class ResponseInstrumentSchema(BaseValidator):
    uuid: str
    instrument_id: str
    name: str
    instrument_type: str
    notes: str
    repair: bool
    active: bool
