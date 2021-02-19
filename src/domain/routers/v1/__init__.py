from fastapi import APIRouter
from domain.routers.v1 import (
    students,
    instruments,
    loans
)

router = APIRouter(
    prefix="/v1"
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
    tags=["Empréstimo - V1"]
)
