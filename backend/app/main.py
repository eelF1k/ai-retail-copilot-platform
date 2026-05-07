from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.api.v1.router import router as v1_router
from app.core.settings import settings
from app.db.sql import Base, engine
from app.observability.logging import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("startup", env=settings.app_env)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as exc:
        # Keep API available in dev even if Postgres is not ready yet.
        logger.warning("postgres_unavailable_on_startup", error=str(exc))
    yield
    logger.info("shutdown")

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(v1_router, prefix=settings.api_prefix)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("request_in", method=request.method, path=request.url.path)
    response = await call_next(request)
    logger.info("request_out", method=request.method, path=request.url.path, status_code=response.status_code)
    return response


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "docs": "/docs",
        "health": f"{settings.api_prefix}/health",
    }

