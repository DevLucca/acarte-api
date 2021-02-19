import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.database import client

def get_application() -> FastAPI:
    client.start()
    client.generate_mapping()

    app = FastAPI(
        title="ACARTE - Instrument Loan", 
        version="0.0.1",
        debug=False,
        openapi_url="/openapi.json"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from domain.routers.v1 import router as v1_router
    app.include_router(v1_router)

    return app

app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "server:app", 
        host="0.0.0.0",
        port=4000,
        reload=True,
        workers=1
        # log_config=dictConfig("json")
    )
