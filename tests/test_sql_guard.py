from app.services.sql_guard import SQLGuard


def test_sql_guard_allows_select_from_whitelisted_tables():
    guard = SQLGuard()
    allowed, reason = guard.validate("SELECT sku, quantity FROM sale_items")
    assert allowed is True
    assert reason == "ok"


def test_sql_guard_blocks_non_select_statements():
    guard = SQLGuard()
    allowed, reason = guard.validate("DELETE FROM sales WHERE id = 1")
    assert allowed is False
    assert "Only SELECT" in reason


def test_sql_guard_blocks_unknown_tables():
    guard = SQLGuard()
    allowed, reason = guard.validate("SELECT * FROM users")
    assert allowed is False
    assert "not allowed" in reason

