from fastapi import APIRouter
from .routers.auth import router as auth_router
from .routers.users import router as users_router
from .routers.students import router as students_router
from .routers.instruments import router as instruments_router
from .routers.loans import router as loans_router

router = APIRouter()

router.include_router(
    auth_router,
    tags=["Autenticação"]
)

# router.include_router(
#     users_router,
#     prefix="/users",
#     tags=["Usuários"]
# )

# router.include_router(
#     students_router,
#     prefix="/students",
#     tags=["Alunos"]
# )

# router.include_router(
#     instruments_router,
#     prefix="/instruments",
#     tags=["Instrumentos"]
# )

# router.include_router(
#     loans_router,
#     prefix="/loans",
#     tags=["Empréstimo dos instrumentos"]
# )
