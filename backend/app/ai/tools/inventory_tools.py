from app.ai.tools.base import BaseTool, ToolDefinition, ToolResult
from app.services.inventory_service import InventoryService
from app.services.analytics_service import AnalyticsService


class GetInventorySummaryTool(BaseTool):
    definition = ToolDefinition(
        name="get_inventory_summary",
        description="Get aggregate inventory statistics across all warehouses",
        business_domain="inventory",
        required_permissions=["Inventory.Read"],
        parameters={"warehouse_id": "Optional UUID to filter by warehouse"},
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, warehouse_id: str | None = None, **kwargs) -> ToolResult:
        from uuid import UUID
        data = await self.svc.get_inventory_analytics(UUID(warehouse_id) if warehouse_id else None)
        return ToolResult(success=True, data=data)


class GetLowStockProductsTool(BaseTool):
    definition = ToolDefinition(
        name="get_low_stock_products",
        description="List products at or below reorder level",
        business_domain="inventory",
        required_permissions=["Inventory.Read"],
    )

    def __init__(self, db):
        self.svc = InventoryService(db)

    async def execute(self, **kwargs) -> ToolResult:
        items = await self.svc.get_low_stock()
        data = [{"inventory_id": str(i.id), "product_id": str(i.product_id),
                 "available": i.available_quantity, "reorder_level": i.reorder_level}
                for i in items]
        return ToolResult(success=True, data=data)


class GetStockoutRiskTool(BaseTool):
    definition = ToolDefinition(
        name="get_stockout_risk",
        description="Identify products at risk of stocking out",
        business_domain="inventory",
        required_permissions=["Inventory.Read"],
    )

    def __init__(self, db):
        self.db = db

    async def execute(self, **kwargs) -> ToolResult:
        from sqlalchemy import select
        from app.models.inventory.inventory import Inventory
        items = (await self.db.execute(
            select(Inventory).where(Inventory.available_quantity.between(1, 50)).limit(20)
        )).scalars().all()
        data = [{"inventory_id": str(i.id), "available": i.available_quantity} for i in items]
        return ToolResult(success=True, data=data)


class GetInventoryHistoryTool(BaseTool):
    definition = ToolDefinition(
        name="get_inventory_history",
        description="Get transaction history for a specific inventory record",
        business_domain="inventory",
        required_permissions=["Inventory.ViewHistory"],
        parameters={"inventory_id": "UUID of the inventory record"},
    )

    def __init__(self, db):
        self.svc = InventoryService(db)

    async def execute(self, inventory_id: str, **kwargs) -> ToolResult:
        from uuid import UUID
        txns = await self.svc.get_transaction_history(UUID(inventory_id))
        data = [{"type": t.transaction_type.value, "before": t.before_quantity,
                 "after": t.after_quantity, "change": t.quantity_change,
                 "reason": t.reason, "date": t.created_at.isoformat()} for t in txns]
        return ToolResult(success=True, data=data)


class GetExpiringStockTool(BaseTool):
    definition = ToolDefinition(
        name="get_expiring_stock",
        description="List inventory expiring within N days",
        business_domain="inventory",
        required_permissions=["Inventory.Read"],
        parameters={"days": "Number of days to look ahead (default: 30)"},
    )

    def __init__(self, db):
        self.svc = InventoryService(db)

    async def execute(self, days: int = 30, **kwargs) -> ToolResult:
        items = await self.svc.get_expiring(days)
        data = [{"inventory_id": str(i.id), "expiry_date": str(i.expiry_date),
                 "available": i.available_quantity} for i in items]
        return ToolResult(success=True, data=data)
