from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.core.database import engine
from app.models.base import Base

app = FastAPI()

app.include_router(auth_router)


@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
