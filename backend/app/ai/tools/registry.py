
from app.ai.tools.base import BaseTool, ToolDefinition


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, type[BaseTool]] = {}

    def register(self, tool_class: type[BaseTool]) -> None:
        self._tools[tool_class.definition.name] = tool_class

    def discover(self) -> list[ToolDefinition]:
        return [cls.definition for cls in self._tools.values()]

    def get_tool(self, name: str) -> type[BaseTool] | None:
        return self._tools.get(name)

    def list_by_domain(self, domain: str) -> list[ToolDefinition]:
        return [cls.definition for cls in self._tools.values()
                if cls.definition.business_domain == domain]

    def list_by_permission(self, permission: str) -> list[ToolDefinition]:
        return [cls.definition for cls in self._tools.values()
                if permission in cls.definition.required_permissions]

    def count(self) -> int:
        return len(self._tools)


# Global registry instance
tool_registry = ToolRegistry()


def register_tools():
    """Auto-discover and register all tools."""
    from app.ai.tools.analytics_tools import ComparePeriodsTool, TopProductsTool, TrendAnalysisTool
    from app.ai.tools.executive_tools import BusinessHealthTool, KPISummaryTool, TopRisksTool
    from app.ai.tools.inventory_tools import (
        GetExpiringStockTool,
        GetInventoryHistoryTool,
        GetInventorySummaryTool,
        GetLowStockProductsTool,
        GetStockoutRiskTool,
    )
    from app.ai.tools.procurement_tools import (
        PendingApprovalsTool,
        ProcurementSpendTool,
        PurchaseOrderSummaryTool,
    )
    from app.ai.tools.supplier_tools import SupplierPerformanceTool, SupplierScorecardTool
    from app.ai.tools.warehouse_tools import WarehouseSummaryTool, WarehouseUtilizationTool

    tools = [
        GetInventorySummaryTool, GetLowStockProductsTool, GetStockoutRiskTool,
        GetInventoryHistoryTool, GetExpiringStockTool,
        BusinessHealthTool, KPISummaryTool, TopRisksTool,
        PurchaseOrderSummaryTool, PendingApprovalsTool, ProcurementSpendTool,
        SupplierScorecardTool, SupplierPerformanceTool,
        WarehouseUtilizationTool, WarehouseSummaryTool,
        TrendAnalysisTool, TopProductsTool, ComparePeriodsTool,
    ]
    for tool_cls in tools:
        tool_registry.register(tool_cls)

    return tool_registry
