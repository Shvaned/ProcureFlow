"""NL→SQL Copilot Service — orchestrates intent → SQL → validation → execution → formatting."""
import json, time
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.services.ai_service import AIService
from app.ai.nl_sql.schema_whitelist import get_schema_context
from app.ai.nl_sql.sql_validator import SQLValidator
from app.ai.nl_sql.query_executor import QueryExecutor, detect_chart_type
from app.core.logging import get_logger

logger = get_logger(__name__)

_conversation_context: list[dict] = []


class NLSQLCopilot:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = AIService()
        self.validator = SQLValidator()
        self.executor = QueryExecutor(db)

    async def process_question(self, question: str, user_id: str = "anonymous") -> dict:
        start_time = time.time()
        schema = get_schema_context()

        # Build conversation context for follow-ups
        global _conversation_context
        history = "\n".join([f"Q: {c['q']}\nA: {c.get('sql', '')}" for c in _conversation_context[-3:]])

        # Step 1: AI generates SQL from natural language
        prompt = f"""You are an analytics SQL assistant for a procurement ERP.

DATABASE SCHEMA:
{schema}

PREVIOUS CONVERSATION:
{history if history else "None"}

USER QUESTION: {question}

Generate a PostgreSQL SELECT query to answer this question.
RULES:
- ONLY SELECT statements
- Use parameterized column names from the whitelist
- Use appropriate aggregations (COUNT, SUM, AVG, MIN, MAX)
- Include GROUP BY when using aggregations
- Use ORDER BY for ranking
- Add LIMIT of 100 max
- NEVER use INSERT, UPDATE, DELETE, DROP, ALTER
- Do NOT use UNION, subqueries, or window functions unless absolutely needed
- Return ONLY the SQL query. No explanations. No markdown."""

        sql = ""
        try:
            raw = await self.ai.explain_business_context(
                context={"schema": schema, "question": question, "history": history},
                question=prompt,
            )
            sql = raw.strip().strip("`").strip("sql").strip()
            if not sql.upper().startswith("SELECT") and not sql.upper().startswith("WITH"):
                sql = f"-- Could not generate valid SQL for: {question}"
        except Exception as e:
            sql = f"-- AI generation failed: {e}"

        # Step 2: Validate SQL
        validation = self.validator.validate(sql)

        # Step 3: Execute if valid
        result = None
        chart_type = "table"
        ai_explanation = ""
        if validation.valid:
            result = await self.executor.execute(sql)
            if result.rows:
                chart_type = detect_chart_type(result.columns, result.rows)

                # Step 4: AI explanation of results
                try:
                    sample = json.dumps(result.rows[:5], default=str)
                    ai_explanation = await self.ai.explain_business_context(
                        context={"question": question, "results_sample": sample, "row_count": result.row_count},
                        question="Summarize these query results in 2-3 sentences. Focus on key findings and business implications.",
                    )
                except Exception:
                    ai_explanation = f"Query returned {result.row_count} rows."

        _conversation_context.append({"q": question, "sql": sql})
        if len(_conversation_context) > 20:
            _conversation_context.pop(0)

        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "question": question,
            "sql_generated": sql,
            "sql_valid": validation.valid,
            "validation_errors": validation.errors,
            "tables_used": validation.tables,
            "columns": result.columns if result else [],
            "rows": result.rows if result else [],
            "row_count": result.row_count if result else 0,
            "execution_ms": result.execution_ms if result else 0,
            "chart_type": chart_type,
            "ai_explanation": ai_explanation,
            "total_latency_ms": latency_ms,
            "suggested_followups": self._generate_followups(question, validation.tables),
        }

    def _generate_followups(self, question: str, tables: list[str]) -> list[str]:
        followups = []
        q_lower = question.lower()
        if "inventory" in q_lower:
            followups.append("Show inventory by warehouse")
            followups.append("Which products are low in stock?")
        if "supplier" in q_lower or "spend" in q_lower:
            followups.append("Compare this quarter vs last quarter")
            followups.append("Show top suppliers by rating")
        if "purchase" in q_lower or "po" in q_lower or "order" in q_lower:
            followups.append("Which POs are overdue?")
            followups.append("Show PO spend by supplier")
        if not followups:
            followups = ["Show inventory value by warehouse", "Which suppliers are top performers?",
                          "Show procurement spend trend", "What products are overstocked?"]
        return followups[:3]
