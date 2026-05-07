from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(v1_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "docs": "/docs",
        "health": f"{settings.api_prefix}/health",
    }

