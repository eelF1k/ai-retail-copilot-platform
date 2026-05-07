class NL2SQLService:
    def translate(self, question: str) -> str:
        q = question.strip().lower()

        if "top sku" in q or "топ sku" in q or "best sku" in q:
            return (
                "SELECT si.sku, MAX(si.product_name) AS product_name, "
                "SUM(si.quantity) AS units_sold, "
                "ROUND(SUM(si.quantity * si.unit_price)::numeric, 2) AS revenue "
                "FROM sale_items si "
                "JOIN sales s ON s.id = si.sale_id "
                "WHERE s.sold_at >= NOW() - INTERVAL '30 day' "
                "GROUP BY si.sku "
                "ORDER BY units_sold DESC"
            )

        if "revenue" in q or "вируч" in q or "дохід" in q:
            return (
                "SELECT s.store_code, "
                "ROUND(SUM(s.total_amount)::numeric, 2) AS revenue, "
                "COUNT(*) AS orders "
                "FROM sales s "
                "WHERE s.sold_at >= NOW() - INTERVAL '30 day' "
                "GROUP BY s.store_code "
                "ORDER BY revenue DESC"
            )

        if "category" in q or "категор" in q:
            return (
                "SELECT si.category, "
                "SUM(si.quantity) AS units_sold, "
                "ROUND(SUM(si.quantity * si.unit_price)::numeric, 2) AS revenue "
                "FROM sale_items si "
                "JOIN sales s ON s.id = si.sale_id "
                "WHERE s.sold_at >= NOW() - INTERVAL '30 day' "
                "GROUP BY si.category "
                "ORDER BY revenue DESC"
            )

        return (
            "SELECT s.store_code, s.order_number, s.sold_at, s.total_amount "
            "FROM sales s "
            "ORDER BY s.sold_at DESC"
        )

