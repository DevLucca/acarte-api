from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .domain.routers.health import api as health_router
from .domain.routers.v1 import router as v1_router

api = FastAPI(
    title="ACARTE - Instrument Loan", 
    version="0.0.1",
    debug=False,
    openapi_url="/openapi.json"
)

api.include_router(v1_router)
api.include_router(health_router)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
