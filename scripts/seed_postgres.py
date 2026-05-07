import asyncio
from datetime import datetime, timedelta, timezone
from random import Random

from app.db.sql import SessionLocal
from app.models.sales import Sale, SaleItem


def _sample_data() -> list[Sale]:
    rnd = Random(42)
    stores = ["VELMART_KYIV", "VELYKA_KYSHENYA_LVIV", "VK_EXPRESS_DNIPRO"]
    products = [
        ("SKU-1001", "Milk 2.5%", "dairy", 42.5),
        ("SKU-1002", "Eggs C1", "dairy", 79.9),
        ("SKU-1003", "Bread Classic", "bakery", 26.0),
        ("SKU-1004", "Chicken Fillet", "meat", 189.0),
        ("SKU-1005", "Apples", "fruits", 49.5),
    ]
    now = datetime.now(tz=timezone.utc)
    sales: list[Sale] = []

    for i in range(1, 61):
        sold_at = now - timedelta(hours=i * 6)
        store = stores[i % len(stores)]
        item_count = rnd.randint(2, 4)
        selected = [products[(i + j) % len(products)] for j in range(item_count)]
        items: list[SaleItem] = []
        total = 0.0
        for sku, name, category, price in selected:
            qty = rnd.randint(1, 5)
            total += qty * price
            items.append(
                SaleItem(
                    sku=sku,
                    product_name=name,
                    category=category,
                    quantity=qty,
                    unit_price=price,
                )
            )
        sales.append(
            Sale(
                store_code=store,
                order_number=f"RG-{10000 + i}",
                sold_at=sold_at,
                total_amount=round(total, 2),
                items=items,
            )
        )
    return sales


async def seed() -> None:
    async with SessionLocal() as session:
        session.add_all(_sample_data())
        await session.commit()
    print("Seeded 60 sales orders")


if __name__ == "__main__":
    asyncio.run(seed())

