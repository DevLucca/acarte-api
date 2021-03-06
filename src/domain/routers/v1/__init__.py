from domain.controllers.auth import AuthController
from fastapi import (
    APIRouter, 
    Depends
)
from domain.routers.v1 import (
    instruments,
    students,
    loans,
    users,
)
from domain.controllers.auth import AuthController

router = APIRouter(
    prefix="/v1",
    dependencies=[Depends(AuthController.scan_token)]
)

router.include_router(
    instruments.router,
    prefix="/instruments",
    tags=["Instrumentos - V1"]
)

router.include_router(
    students.router,
    prefix="/students",
    tags=["Alunos - V1"]
)

router.include_router(
    loans.router,
    prefix="/loans",
    tags=["Empréstimos - V1"]
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["Users - V1"]
)
