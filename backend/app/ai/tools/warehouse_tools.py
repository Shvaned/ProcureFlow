from app.ai.tools.base import BaseTool, ToolDefinition, ToolResult
from app.services.analytics_service import AnalyticsService


class WarehouseSummaryTool(BaseTool):
    definition = ToolDefinition(
        name="warehouse_summary",
        description="Get inventory value and utilization for each warehouse",
        business_domain="warehouse",
        required_permissions=["Warehouses.Read", "Analytics.Read"],
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, **kwargs) -> ToolResult:
        data = await self.svc.get_warehouse_analytics()
        return ToolResult(success=True, data=data)


class WarehouseUtilizationTool(BaseTool):
    definition = ToolDefinition(
        name="warehouse_utilization",
        description="Get detailed warehouse utilization metrics",
        business_domain="warehouse",
        required_permissions=["Warehouses.Read"],
    )

    def __init__(self, db):
        self.db = db

    async def execute(self, **kwargs) -> ToolResult:
        from sqlalchemy import select, func
        from app.models.inventory.inventory import Inventory
        rows = (await self.db.execute(
            select(Inventory.warehouse_id, func.count(Inventory.id), func.sum(Inventory.available_quantity))
            .group_by(Inventory.warehouse_id)
        )).all()
        data = [{"warehouse_id": str(r[0]), "inventory_records": r[1], "total_quantity": int(r[2] or 0)}
                for r in rows]
        return ToolResult(success=True, data=data)
