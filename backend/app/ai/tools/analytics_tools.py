from app.ai.tools.base import BaseTool, ToolDefinition, ToolResult
from app.services.analytics_service import AnalyticsService


class TrendAnalysisTool(BaseTool):
    definition = ToolDefinition(
        name="trend_analysis",
        description="Analyze trends across key business metrics",
        business_domain="analytics",
        required_permissions=["AI.Use", "Analytics.Read"],
        parameters={"metric": "KPI key to analyze trend for"},
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, metric: str = "inventory_turnover", **kwargs) -> ToolResult:
        kpi = await self.svc.get_kpi_data(metric)
        return ToolResult(success=True, data=kpi)


class TopProductsTool(BaseTool):
    definition = ToolDefinition(
        name="top_products",
        description="Get product analytics including category and brand breakdowns",
        business_domain="analytics",
        required_permissions=["AI.Use", "Analytics.Read"],
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, **kwargs) -> ToolResult:
        data = await self.svc.get_product_analytics()
        return ToolResult(success=True, data=data)


class ComparePeriodsTool(BaseTool):
    definition = ToolDefinition(
        name="compare_periods",
        description="Compare key metrics between current and previous period",
        business_domain="analytics",
        required_permissions=["AI.Use", "Analytics.Read"],
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, **kwargs) -> ToolResult:
        current = await self.svc.get_executive_summary()
        return ToolResult(success=True, data={"current_period": current, "note": "Historical comparison requires time-series data"})
