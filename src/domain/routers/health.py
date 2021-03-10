from domain.routers import BaseRouter

api = BaseRouter(
    prefix="/health",
    tags=["Health"]
)

api.get("/",
        response_model=None,
        name="Health Route",
        summary="Checar status da API"
    )(lambda : {'ok':True})
