from sqlalchemy import text

from app.db.sql import SessionLocal


class RetailAnalyticsRepository:
    async def revenue_by_store(self, days: int = 30) -> list[dict]:
        query = text(
            """
            SELECT
                s.store_code,
                ROUND(SUM(s.total_amount)::numeric, 2) AS revenue,
                COUNT(*) AS orders
            FROM sales s
            WHERE s.sold_at >= NOW() - (:days * INTERVAL '1 day')
            GROUP BY s.store_code
            ORDER BY revenue DESC
            """
        )
        async with SessionLocal() as session:
            result = await session.execute(query, {"days": days})
            rows = result.mappings().all()
        return [dict(row) for row in rows]

    async def top_skus(self, days: int = 30, limit: int = 10) -> list[dict]:
        query = text(
            """
            SELECT
                si.sku,
                MAX(si.product_name) AS product_name,
                SUM(si.quantity) AS units_sold,
                ROUND(SUM(si.quantity * si.unit_price)::numeric, 2) AS revenue
            FROM sale_items si
            JOIN sales s ON s.id = si.sale_id
            WHERE s.sold_at >= NOW() - (:days * INTERVAL '1 day')
            GROUP BY si.sku
            ORDER BY units_sold DESC
            LIMIT :limit
            """
        )
        async with SessionLocal() as session:
            result = await session.execute(query, {"days": days, "limit": limit})
            rows = result.mappings().all()
        return [dict(row) for row in rows]

