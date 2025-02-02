from fastapi import APIRouter
from api.config.settings import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@router.get("/readiness")
async def readiness_check():
    return {
        "status": "ready",
        "services": {
            "terraform": "available",
            "ansible": "available",
            "aws": "connected"
        }
    }