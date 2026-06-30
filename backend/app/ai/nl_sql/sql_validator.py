"""SQL validation — ensures only safe SELECT queries against whitelisted tables."""
import re

from app.ai.nl_sql.schema_whitelist import UNSAFE_KEYWORDS, validate_table


class SQLValidationResult:
    def __init__(self, valid: bool, sql: str = "", errors: list[str] | None = None, tables: list[str] | None = None):
        self.valid = valid
        self.sql = sql
        self.errors = errors or []
        self.tables = tables or []


class SQLValidator:
    MAX_ROWS = 1000
    MAX_QUERY_LENGTH = 4000

    def validate(self, sql: str) -> SQLValidationResult:
        errors: list[str] = []
        sql_upper = sql.upper().strip()

        if not sql_upper:
            errors.append("Empty query")
            return SQLValidationResult(False, sql, errors)

        if len(sql) > self.MAX_QUERY_LENGTH:
            errors.append(f"Query too long ({len(sql)} > {self.MAX_QUERY_LENGTH} chars)")

        if not sql_upper.startswith("SELECT") and not sql_upper.startswith("WITH"):
            errors.append("Only SELECT queries are allowed")

        for keyword in UNSAFE_KEYWORDS:
            if re.search(rf"\b{keyword}\b", sql_upper):
                errors.append(f"Unsafe keyword detected: {keyword}")

        tables = self._extract_tables(sql)
        for table in tables:
            if not validate_table(table):
                errors.append(f"Table not allowed: {table}")

        if errors:
            return SQLValidationResult(False, sql, errors)
        return SQLValidationResult(True, sql, tables=tables)

    def _extract_tables(self, sql: str) -> list[str]:
        """Extract table names from FROM and JOIN clauses."""
        sql_lower = sql.lower()
        tables = []
        # Simple extraction: words after FROM or JOIN
        for match in re.finditer(r'\b(?:from|join)\s+(\w+)', sql_lower):
            tables.append(match.group(1))
        return list(set(tables))
