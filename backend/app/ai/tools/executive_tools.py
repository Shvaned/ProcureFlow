from app.ai.tools.base import BaseTool, ToolDefinition, ToolResult
from app.services.analytics_service import AnalyticsService


class BusinessHealthTool(BaseTool):
    definition = ToolDefinition(
        name="business_health",
        description="Get high-level business health metrics including inventory value, open POs, supplier counts",
        business_domain="executive",
        required_permissions=["AI.Use", "Analytics.Read"],
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, **kwargs) -> ToolResult:
        data = await self.svc.get_executive_summary()
        return ToolResult(success=True, data=data)


class KPISummaryTool(BaseTool):
    definition = ToolDefinition(
        name="kpi_summary",
        description="Get detailed KPI values for a specific metric",
        business_domain="executive",
        required_permissions=["AI.Use", "Analytics.Read"],
        parameters={"kpi_key": "KPI identifier (e.g., inventory_turnover, fill_rate, supplier_otif)"},
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, kpi_key: str = "inventory_turnover", **kwargs) -> ToolResult:
        data = await self.svc.get_kpi_data(kpi_key)
        return ToolResult(success=True, data=data)


class TopRisksTool(BaseTool):
    definition = ToolDefinition(
        name="top_risks",
        description="Identify the most critical business risks based on current data",
        business_domain="executive",
        required_permissions=["AI.Use", "Analytics.Read"],
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, **kwargs) -> ToolResult:
        exec_data = await self.svc.get_executive_summary()
        low_stock = await self.svc.get_low_stock_summary()
        risks = []
        if exec_data.get("low_stock_items", 0) > 0:
            risks.append({"type": "low_stock", "count": exec_data["low_stock_items"], "severity": "high"})
        if exec_data.get("out_of_stock_items", 0) > 0:
            risks.append({"type": "out_of_stock", "count": exec_data["out_of_stock_items"], "severity": "critical"})
        if exec_data.get("pending_approvals", 0) > 10:
            risks.append({"type": "pending_approvals", "count": exec_data["pending_approvals"], "severity": "medium"})
        if not risks:
            risks.append({"type": "none", "severity": "low", "message": "No critical risks detected"})
        return ToolResult(success=True, data={"risks": risks, "low_stock_detail": low_stock[:5]})
