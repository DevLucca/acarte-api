import uvicorn
from core import cfg
from pony import orm
from fastapi import FastAPI
from routers import router

db = orm.Database()
db.bind(
    provider='mysql',
    host=cfg["db-location"]["value"],
    port=cfg["db-port"]["value"],
    user=cfg["db-user"]["value"],
    passwd=cfg["db-password"]["value"],
    db=cfg["db-name"]["value"]
)
db.generate_mapping(create_tables=True)

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
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=cfg["app-port"]["value"] or 4000,
        reload=True
    )
