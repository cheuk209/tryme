from fastapi import FastAPI
from app.api.routes import commodity_data
from app.core.config import settings

app = FastAPI()
app.include_router(commodity_data.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Please hire me"}

