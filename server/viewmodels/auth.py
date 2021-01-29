from pydantic import BaseModel
from pydantic.fields import Field

class TokenSchema(BaseModel):
    access_token: bytes
    expires_in: int = 15*60
    token_type: str = "bearer"

    class Config:
        allow_population_by_field_name = True
