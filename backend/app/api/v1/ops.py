from fastapi import APIRouter, Query

from app.repositories import RetailAnalyticsRepository

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/revenue-by-store")
async def revenue_by_store(days: int = Query(30, ge=1, le=365)):
    data = await RetailAnalyticsRepository().revenue_by_store(days=days)
    return {"days": days, "rows": data}


@router.get("/top-skus")
async def top_skus(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=100),
):
    data = await RetailAnalyticsRepository().top_skus(days=days, limit=limit)
    return {"days": days, "limit": limit, "rows": data}

