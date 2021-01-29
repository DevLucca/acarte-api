import os
import uvicorn
from server import router as v1
from fastapi import FastAPI

app = FastAPI(
    title="ACARTE - Instrument Loan App", 
    version="0.0.1",
    debug=True)

app.include_router(
    v1,
    prefix="/v1"
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=os.getenv("PORT", 4000), 
        reload=True
    )