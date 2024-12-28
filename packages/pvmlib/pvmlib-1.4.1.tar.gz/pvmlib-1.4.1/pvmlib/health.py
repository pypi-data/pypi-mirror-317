from fastapi import APIRouter, HTTPException
from .database import database_manager

health_router = APIRouter()

@health_router.get("/health/liveness")
async def liveness():
    return {"status": "UP"}

@health_router.get("/health/readiness")
async def readiness():
    try:
        await database_manager.mongo_database.command("ping")
        return {"status": "UP"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {e}")