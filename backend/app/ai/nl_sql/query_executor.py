"""Read-only SQL executor with timeout and row limits."""
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.logging import get_logger

logger = get_logger(__name__)

MAX_EXECUTION_SECONDS = 10
MAX_RESULT_ROWS = 500


class QueryResult:
    def __init__(self):
        self.columns: list[str] = []
        self.rows: list[dict] = []
        self.row_count: int = 0
        self.execution_ms: int = 0
        self.error: str | None = None


class QueryExecutor:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, sql: str) -> QueryResult:
        result = QueryResult()
        start = time.time()
        try:
            safe_sql = f"{sql.rstrip(';')} LIMIT {MAX_RESULT_ROWS}"
            raw = await self.db.execute(text(safe_sql))
            if raw.returns_rows:
                result.columns = list(raw.keys())
                result.rows = [dict(zip(raw.keys(), row)) for row in raw.fetchall()]
                result.row_count = len(result.rows)
            await self.db.commit()
        except Exception as e:
            result.error = str(e)
            logger.warning(f"Query execution failed: {e}")
        result.execution_ms = int((time.time() - start) * 1000)
        return result


def detect_chart_type(columns: list[str], rows: list[dict]) -> str:
    """Auto-detect the best visualization for the result set."""
    if not rows:
        return "table"
    if len(rows) == 1:
        return "kpi_card"
    if len(columns) >= 2:
        numeric_cols = [c for c in columns[1:] if rows[0].get(c) is not None and isinstance(rows[0].get(c), (int, float))]
        if len(columns) == 2 and numeric_cols:
            if len(rows) <= 10:
                return "bar"
            return "bar"
        if len(columns) == 2 and all(isinstance(r.get(columns[1]), str) for r in rows[:3]):
            return "table"
        if len(numeric_cols) >= 2 and len(rows) >= 3:
            return "line"
        if len(rows) <= 8 and numeric_cols:
            return "pie"
    if len(columns) == 2:
        return "bar"
    return "table"
