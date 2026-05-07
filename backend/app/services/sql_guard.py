import re


class SQLGuard:
    _DENY_KEYWORDS = (
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "grant ",
        "revoke ",
        "copy ",
    )

    _ALLOWED_TABLES = {"sales", "sale_items"}

    def validate(self, sql: str) -> tuple[bool, str]:
        normalized = self._normalize(sql)
        if not normalized.startswith("select "):
            return False, "Only SELECT statements are allowed"

        if ";" in normalized:
            return False, "Multiple statements are not allowed"

        for keyword in self._DENY_KEYWORDS:
            if keyword in normalized:
                return False, f"Forbidden keyword detected: {keyword.strip()}"

        tables = self._extract_tables(normalized)
        if not tables:
            return False, "No known source table found"

        unknown = [table for table in tables if table not in self._ALLOWED_TABLES]
        if unknown:
            return False, f"Table(s) not allowed: {', '.join(sorted(set(unknown)))}"

        return True, "ok"

    @staticmethod
    def _normalize(sql: str) -> str:
        return " ".join(sql.strip().lower().split())

    @staticmethod
    def _extract_tables(sql: str) -> list[str]:
        from_matches = re.findall(r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql)
        join_matches = re.findall(r"\bjoin\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql)
        return from_matches + join_matches

