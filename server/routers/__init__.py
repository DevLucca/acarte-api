from fastapi import APIRouter
from .students import router as students_router
from .instruments import router as instruments_router
from .loans import router as loans_router

router = APIRouter()

router.include_router(
    students_router,
    prefix="/students",
    tags=["Alunos"]
)

router.include_router(
    instruments_router,
    prefix="/instruments",
    tags=["Instrumentos"]
)

router.include_router(
    loans_router,
    prefix="/loans",
    tags=["Empréstimo"]
)
