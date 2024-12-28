from fastapi import APIRouter, HTTPException
from .database import database_manager
import os

health_router = APIRouter()

@health_router.get("/health/liveness")
async def liveness():
    return {"status": "UP"}

@health_router.get("/health/readiness")
async def readiness():
    try:
        database_url = os.getenv("URL_DB")
        if not database_url:
            raise Exception("URL_DB environment variable not found")
        await database_manager.mongo_database.command("ping")
        return {"status": "UP"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {e}")