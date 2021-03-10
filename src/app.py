from fastapi import FastAPI
from core.settings import cfg
from fastapi.middleware import (
    cors,
    trustedhost
)
from fastapi.openapi.utils import get_openapi
from domain.routers.v1 import router as v1_router
from domain.routers.auth import api as auth_router
from domain.routers.health import api as health_router

api = FastAPI(
    title=cfg.app_name.value,
    debug=cfg.app_debug.value
)

api.include_router(auth_router)
api.include_router(health_router)
api.include_router(v1_router)

api.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.add_middleware(
    trustedhost.TrustedHostMiddleware,
    allowed_hosts=cfg.app_allowed_hosts.value
)

def custom_openapi():
    openapi_schema = get_openapi(
        title=f"{cfg.app_name.value} - DOCUMENTATION",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=api.routes,
    )
    api.openapi_schema = openapi_schema
    return api.openapi_schema

api.openapi = custom_openapi
