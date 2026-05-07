from fastapi import APIRouter

from app.core.settings import settings

router = APIRouter()


@router.get("/health", tags=["system"])
async def healthcheck():
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.app_env,
    }


@router.get("/ready", tags=["system"])
async def readiness():
    # Next steps will include real checks for Postgres/Redis/LLM providers.
    return {"ready": True}

