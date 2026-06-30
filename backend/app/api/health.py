from fastapi import APIRouter

from app.core.config import settings
from app.schemas.common import StandardResponse

router = APIRouter()


@router.get("/health", response_model=StandardResponse[dict])
async def health():
    return StandardResponse.ok(
        data={"status": "healthy", "version": settings.APP_VERSION},
        message="Service is healthy",
    )


@router.get("/health/ready", response_model=StandardResponse[dict])
async def readiness():
    return StandardResponse.ok(
        data={"status": "ready"},
        message="Service is ready",
    )


@router.get("/health/live", response_model=StandardResponse[dict])
async def liveness():
    return StandardResponse.ok(
        data={"status": "alive"},
        message="Service is alive",
    )
