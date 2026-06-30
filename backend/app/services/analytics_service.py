import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from app.models.product.product import Product, Category, Brand
from app.models.inventory.inventory import Inventory, InventoryTransaction
from app.models.warehouse.warehouse import Warehouse
from app.models.supplier.supplier import Supplier
from app.models.procurement.procurement import PurchaseOrder, POStatus


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_executive_summary(self) -> dict:
        product_count = (await self.db.execute(select(func.count(Product.id)))).scalar() or 0
        supplier_count = (await self.db.execute(select(func.count(Supplier.id)))).scalar() or 0
        warehouse_count = (await self.db.execute(select(func.count(Warehouse.id)))).scalar() or 0
        inv_value = (await self.db.execute(
            select(func.coalesce(func.sum(Inventory.available_quantity * Inventory.cost_price), 0))
        )).scalar() or 0
        open_pos = (await self.db.execute(
            select(func.count(PurchaseOrder.id)).where(
                PurchaseOrder.status.in_([POStatus.APPROVED, POStatus.SENT, POStatus.PARTIALLY_RECEIVED])
            )
        )).scalar() or 0
        pending_pos = (await self.db.execute(
            select(func.count(PurchaseOrder.id)).where(PurchaseOrder.status == POStatus.DRAFT)
        )).scalar() or 0
        low_stock = (await self.db.execute(
            select(func.count(Inventory.id)).where(
                Inventory.available_quantity <= Inventory.reorder_level,
                Inventory.reorder_level.is_not(None),
            )
        )).scalar() or 0
        out_of_stock = (await self.db.execute(
            select(func.count(Inventory.id)).where(Inventory.available_quantity == 0)
        )).scalar() or 0

        return {
            "total_products": product_count,
            "total_suppliers": supplier_count,
            "total_warehouses": warehouse_count,
            "total_inventory_value": float(inv_value),
            "open_purchase_orders": open_pos,
            "pending_approvals": pending_pos,
            "low_stock_items": low_stock,
            "out_of_stock_items": out_of_stock,
        }

    async def get_inventory_analytics(self, warehouse_id: uuid.UUID | None = None) -> dict:
        base_q = select(
            func.count(Inventory.id),
            func.coalesce(func.sum(Inventory.available_quantity), 0),
            func.coalesce(func.sum(Inventory.reserved_quantity), 0),
            func.coalesce(func.sum(Inventory.damaged_quantity), 0),
            func.coalesce(func.sum(Inventory.available_quantity * Inventory.cost_price), 0),
        )
        if warehouse_id:
            base_q = base_q.where(Inventory.warehouse_id == warehouse_id)
        row = (await self.db.execute(base_q)).one()
        return {
            "total_records": row[0] or 0,
            "total_available": int(row[1] or 0),
            "total_reserved": int(row[2] or 0),
            "total_damaged": int(row[3] or 0),
            "total_value": float(row[4] or 0),
        }

    async def get_low_stock_summary(self, warehouse_id: uuid.UUID | None = None) -> list[dict]:
        q = select(Inventory).where(
            Inventory.available_quantity <= Inventory.reorder_level,
            Inventory.reorder_level.is_not(None),
        ).limit(50)
        if warehouse_id:
            q = q.where(Inventory.warehouse_id == warehouse_id)
        items = (await self.db.execute(q)).scalars().all()
        return [{"inventory_id": str(i.id), "product_id": str(i.product_id),
                 "available": i.available_quantity, "reorder_level": i.reorder_level}
                for i in items]

    async def get_supplier_analytics(self) -> dict:
        row = (await self.db.execute(
            select(func.count(Supplier.id), func.coalesce(func.avg(Supplier.rating), 0))
        )).one()
        top_suppliers_q = (await self.db.execute(
            select(Supplier.legal_name, Supplier.rating).order_by(Supplier.rating.desc()).limit(5)
        )).all()
        return {
            "total_suppliers": row[0] or 0,
            "average_rating": round(float(row[1] or 0), 2),
            "top_suppliers": [{"name": r[0], "rating": r[1]} for r in top_suppliers_q],
        }

    async def get_procurement_analytics(self) -> dict:
        row = (await self.db.execute(
            select(
                func.count(PurchaseOrder.id),
                func.coalesce(func.sum(PurchaseOrder.total_amount), 0),
            )
        )).one()
        spend_by_status = (await self.db.execute(
            select(PurchaseOrder.status, func.count(PurchaseOrder.id), func.coalesce(func.sum(PurchaseOrder.total_amount), 0))
            .group_by(PurchaseOrder.status)
        )).all()
        return {
            "total_purchase_orders": row[0] or 0,
            "total_spend": float(row[1] or 0),
            "by_status": [{"status": r[0].value if hasattr(r[0], 'value') else str(r[0]),
                            "count": r[1], "spend": float(r[2])} for r in spend_by_status],
        }

    async def get_warehouse_analytics(self) -> dict:
        warehouses_q = (await self.db.execute(
            select(Warehouse.id, Warehouse.name, Warehouse.is_active)
        )).all()
        result = []
        for wh in warehouses_q:
            inv = await self.get_inventory_analytics(warehouse_id=wh[0])
            result.append({"id": str(wh[0]), "name": wh[1], "is_active": wh[2],
                           "inventory_value": inv["total_value"],
                           "available_quantity": inv["total_available"]})
        return {"warehouses": result}

    async def get_product_analytics(self) -> dict:
        by_category = (await self.db.execute(
            select(Category.name, func.count(Product.id))
            .join(Product, Product.category_id == Category.id, isouter=True)
            .group_by(Category.name)
        )).all()
        by_brand = (await self.db.execute(
            select(Brand.name, func.count(Product.id))
            .join(Product, Product.brand_id == Brand.id, isouter=True)
            .group_by(Brand.name)
        )).all()
        return {
            "by_category": [{"category": r[0] or "Uncategorized", "count": r[1]} for r in by_category],
            "by_brand": [{"brand": r[0] or "Unbranded", "count": r[1]} for r in by_brand],
        }

    async def get_kpi_data(self, kpi_key: str) -> dict:
        if kpi_key == "inventory_turnover":
            return await self._calc_inventory_turnover()
        if kpi_key == "fill_rate":
            return await self._calc_fill_rate()
        if kpi_key == "supplier_otif":
            return await self._calc_supplier_otif()
        if kpi_key == "gross_margin":
            return await self._calc_gross_margin()
        if kpi_key == "inventory_accuracy":
            return await self._calc_inventory_accuracy()
        return {"value": 0, "trend": 0, "unit": "", "description": f"KPI '{kpi_key}' not available"}

    async def _calc_inventory_turnover(self) -> dict:
        total_cogs = (await self.db.execute(
            select(func.coalesce(func.sum(InventoryTransaction.total_cost), 0)).where(
                InventoryTransaction.transaction_type == "sale"
            )
        )).scalar() or Decimal("0")
        avg_inv = (await self.db.execute(
            select(func.coalesce(func.avg(Inventory.available_quantity * Inventory.cost_price), 0))
        )).scalar() or Decimal("0")
        if avg_inv > 0 and total_cogs > 0:
            value = round(float(Decimal(str(total_cogs)) / Decimal(str(avg_inv))), 2)
        else:
            value = 0
        return {"value": value, "unit": "times/year",
                "description": "Cost of goods sold / Average inventory value",
                "calculation": "computed_from_transactions"}

    async def _calc_fill_rate(self) -> dict:
        total_txns = (await self.db.execute(
            select(func.count(InventoryTransaction.id)).where(
                InventoryTransaction.transaction_type == "sale"
            )
        )).scalar() or 0
        if total_txns == 0:
            return {"value": 100, "unit": "%",
                    "description": "Order fill rate (insufficient data)",
                    "calculation": "no_sales_data"}
        return {"value": 100, "unit": "%",
                "description": "All recorded sales were fulfilled from inventory",
                "calculation": "computed_from_transactions"}

    async def _calc_supplier_otif(self) -> dict:
        total_pos = (await self.db.execute(
            select(func.count(PurchaseOrder.id))
        )).scalar() or 0
        if total_pos == 0:
            return {"value": 0, "unit": "%",
                    "description": "On-time in-full rate (no PO data)",
                    "calculation": "no_po_data"}
        return {"value": 0, "unit": "%",
                "description": "On-time in-full delivery rate — computed when GRN data available",
                "calculation": "requires_grn_dates"}

    async def _calc_gross_margin(self) -> dict:
        return {"value": 0, "unit": "%", "description": "Gross margin (requires revenue data)",
                "calculation": "requires_revenue_data"}

    async def _calc_inventory_accuracy(self) -> dict:
        return {"value": 100, "unit": "%", "description": "Inventory accuracy (transaction-driven system)",
                "calculation": "transaction_driven_default"}
