import argparse
import asyncio
import json

from sqlalchemy import text

from app.db.sql import SessionLocal

QUERIES = {
    "revenue_by_store": """
        SELECT store_id, SUM(total_amount) AS total_revenue
        FROM sales
        WHERE sold_at >= NOW() - INTERVAL '30 day'
        GROUP BY store_id
        ORDER BY total_revenue DESC
        LIMIT 20
    """,
    "top_skus": """
        SELECT si.sku, SUM(si.quantity) AS qty
        FROM sale_items si
        JOIN sales s ON s.id = si.sale_id
        WHERE s.sold_at >= NOW() - INTERVAL '30 day'
        GROUP BY si.sku
        ORDER BY qty DESC
        LIMIT 20
    """,
}


async def build_report() -> list[dict]:
    report: list[dict] = []
    async with SessionLocal() as session:
        for name, sql in QUERIES.items():
            explain_sql = f"EXPLAIN (FORMAT JSON) {sql}"
            row = (await session.execute(text(explain_sql))).scalar_one()
            plan = row[0]["Plan"] if isinstance(row, list) and row else {}
            node_type = plan.get("Node Type", "unknown")
            total_cost = plan.get("Total Cost", 0)
            suggestions = []

            if node_type in {"Seq Scan", "Hash Join"}:
                suggestions.append("Consider adding composite index on filter/join columns.")
            if total_cost and total_cost > 10000:
                suggestions.append("Consider materialized view for heavy dashboard workloads.")
            if not suggestions:
                suggestions.append("Plan looks acceptable for current threshold.")

            report.append(
                {
                    "query": name,
                    "node_type": node_type,
                    "total_cost": total_cost,
                    "suggestions": suggestions,
                }
            )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SQL tuning report from EXPLAIN plans.")
    parser.parse_args()
    payload = asyncio.run(build_report())
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

