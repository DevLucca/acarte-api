from fastapi import Response
from .base import BaseRouter

api = BaseRouter(
    prefix="/health",
    tags=["Health"]
)

api.get("/", name="Health Route", summary="Checar status da API")(lambda : True)
