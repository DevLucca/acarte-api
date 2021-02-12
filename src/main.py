import uvicorn
from fastapi import FastAPI
from core import cfg
from routers import router
from models import DBClient


app = FastAPI(
    title="ACARTE - Instrument Loan", 
    version="0.0.1",
    debug=cfg["app-debug"]["value"]
)

app.include_router(
    router,
    prefix='/v1'
)

if __name__ == "__main__":
    DBClient.initialize()
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=cfg["app-port"]["value"] or 4000,
        reload=True
    )
