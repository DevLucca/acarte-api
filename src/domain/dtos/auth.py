from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: bytes
    expires_in: int = 15*60
    token_type: str = "bearer"
    # refresh_token: bytes

    class Config:
        allow_population_by_field_name = True
