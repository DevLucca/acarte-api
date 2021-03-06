from fastapi import APIRouter
from . import (
    instruments
)

router = APIRouter(
    prefix="/v1"
)

router.include_router(
    instruments.router,
    prefix="/instruments",
    tags=["Instrumentos - V1"]
)
