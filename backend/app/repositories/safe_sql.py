from sqlalchemy import text

from app.db.sql import SessionLocal


class SafeSQLRepository:
    async def execute_select(self, sql: str, max_rows: int = 200) -> list[dict]:
        limited_sql = f"""
        SELECT * FROM (
            {sql}
        ) AS _safe_query
        LIMIT :max_rows
        """
        async with SessionLocal() as session:
            result = await session.execute(text(limited_sql), {"max_rows": max_rows})
            rows = result.mappings().all()
        return [dict(row) for row in rows]

