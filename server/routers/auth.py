from . import CustomRouter
from fastapi.security import OAuth2PasswordRequestForm
from ..controllers.auth import AuthController
from ..viewmodels.auth import (
    TokenSchema
)
from fastapi import (
    Depends,
    Body,
    Path,
    Header
)

router = CustomRouter()

@router.post("/token", response_model=TokenSchema, summary="Autenticação")
async def authenticate(user_data: OAuth2PasswordRequestForm = Depends()):
    return AuthController.authenticate(user_data.username, user_data.password, user_data.client_id, user_data.client_secret)
