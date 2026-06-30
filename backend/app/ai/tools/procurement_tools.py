from app.ai.tools.base import BaseTool, ToolDefinition, ToolResult
from app.services.analytics_service import AnalyticsService


class PurchaseOrderSummaryTool(BaseTool):
    definition = ToolDefinition(
        name="purchase_order_summary",
        description="Get summary of purchase orders with counts by status and total spend",
        business_domain="procurement",
        required_permissions=["PurchaseOrders.Read", "Analytics.Read"],
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, **kwargs) -> ToolResult:
        data = await self.svc.get_procurement_analytics()
        return ToolResult(success=True, data=data)


class PendingApprovalsTool(BaseTool):
    definition = ToolDefinition(
        name="pending_approvals",
        description="List purchase orders pending approval",
        business_domain="procurement",
        required_permissions=["PurchaseOrders.Read"],
    )

    def __init__(self, db):
        self.db = db

    async def execute(self, **kwargs) -> ToolResult:
        from sqlalchemy import select

        from app.models.procurement.procurement import POStatus, PurchaseOrder
        pos = (await self.db.execute(
            select(PurchaseOrder).where(PurchaseOrder.status == POStatus.DRAFT).limit(20)
        )).scalars().all()
        data = [{"po_number": po.po_number, "total": float(po.total_amount),
                 "date": po.created_at.isoformat()} for po in pos]
        return ToolResult(success=True, data=data)


class ProcurementSpendTool(BaseTool):
    definition = ToolDefinition(
        name="procurement_spend",
        description="Get procurement spend summary by status",
        business_domain="procurement",
        required_permissions=["PurchaseOrders.Read", "Analytics.Read"],
    )

    def __init__(self, db):
        self.svc = AnalyticsService(db)

    async def execute(self, **kwargs) -> ToolResult:
        data = await self.svc.get_procurement_analytics()
        return ToolResult(success=True, data={"spend": data})
