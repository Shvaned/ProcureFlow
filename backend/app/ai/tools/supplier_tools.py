from app.ai.tools.base import BaseTool, ToolDefinition, ToolResult
from app.services.procurement_service import SupplierService


class SupplierScorecardTool(BaseTool):
    definition = ToolDefinition(
        name="supplier_scorecard",
        description="Get performance scorecard for a supplier including ratings and delivery metrics",
        business_domain="supplier",
        required_permissions=["Suppliers.Read"],
        parameters={"supplier_id": "UUID of the supplier"},
    )

    def __init__(self, db):
        self.svc = SupplierService(db)

    async def execute(self, supplier_id: str, **kwargs) -> ToolResult:
        from uuid import UUID
        supplier = await self.svc.get_supplier(UUID(supplier_id))
        data = {
            "id": str(supplier.id), "legal_name": supplier.legal_name,
            "rating": supplier.rating, "country": supplier.country,
            "is_preferred": supplier.is_preferred, "contacts": len(supplier.contacts),
        }
        return ToolResult(success=True, data=data)


class SupplierPerformanceTool(BaseTool):
    definition = ToolDefinition(
        name="supplier_performance",
        description="Get performance metrics for all suppliers ranked by rating",
        business_domain="supplier",
        required_permissions=["Suppliers.Read"],
    )

    def __init__(self, db):
        self.db = db

    async def execute(self, **kwargs) -> ToolResult:
        from sqlalchemy import select
        from app.models.supplier.supplier import Supplier
        suppliers = (await self.db.execute(
            select(Supplier).order_by(Supplier.rating.desc()).limit(10)
        )).scalars().all()
        data = [{"legal_name": s.legal_name, "rating": s.rating, "country": s.country}
                for s in suppliers]
        return ToolResult(success=True, data=data)
