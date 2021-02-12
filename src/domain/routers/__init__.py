from fastapi import APIRouter
from domain.routers import (
    students,
    instruments,
    loans
)

router = APIRouter()

router.include_router(
    students.router,
    prefix="/students",
    tags=["Alunos"]
)

router.include_router(
    instruments.router,
    prefix="/instruments",
    tags=["Instrumentos"]
)

router.include_router(
    loans.router,
    prefix="/loans",
    tags=["Empréstimo"]
)
