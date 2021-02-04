from os import getenv
import uvicorn
from server import routers
from fastapi import FastAPI
from core import cfg
from repository import DBClient
# DBClient.initialize()

app = FastAPI(
    title="ACARTE - Instrument Loan", 
    version="0.0.1",
    debug=cfg["app-debug"]["value"]
)

app.include_router(
    routers.router
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=cfg["app-port"]["value"],
        reload=True
    )
