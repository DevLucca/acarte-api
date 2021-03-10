from domain.routers import BaseRouter
from domain.dtos.auth import TokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from domain.controllers.auth import AuthController

controller = AuthController()

api = BaseRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

api.post("/login",
        response_model=TokenSchema,
        name="Auth Route",
        summary="Autenticar usuário"
    )(controller.authenticate)

api.post("/renew",
        response_model=TokenSchema,
        name="Auth Renew Route",
        summary="Renovar autenticação usuário"
    )(lambda : {'ok':True})