from fastapi import FastAPI
from routers.networks import router as networks_router
from pydantic import BaseModel

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(networks_router)