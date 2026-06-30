from typing import Type
from app.ai.tools.base import BaseTool, ToolDefinition, ToolResult


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Type[BaseTool]] = {}

    def register(self, tool_class: Type[BaseTool]) -> None:
        self._tools[tool_class.definition.name] = tool_class

    def discover(self) -> list[ToolDefinition]:
        return [cls.definition for cls in self._tools.values()]

    def get_tool(self, name: str) -> Type[BaseTool] | None:
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
    from app.ai.tools.inventory_tools import (
        GetInventorySummaryTool, GetLowStockProductsTool,
        GetStockoutRiskTool, GetInventoryHistoryTool, GetExpiringStockTool,
    )
    from app.ai.tools.executive_tools import (
        BusinessHealthTool, KPISummaryTool, TopRisksTool,
    )
    from app.ai.tools.procurement_tools import (
        PurchaseOrderSummaryTool, PendingApprovalsTool, ProcurementSpendTool,
    )
    from app.ai.tools.supplier_tools import (
        SupplierScorecardTool, SupplierPerformanceTool,
    )
    from app.ai.tools.warehouse_tools import (
        WarehouseUtilizationTool, WarehouseSummaryTool,
    )
    from app.ai.tools.analytics_tools import (
        TrendAnalysisTool, TopProductsTool, ComparePeriodsTool,
    )

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
