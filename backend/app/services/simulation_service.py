import random
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.inventory.inventory import Inventory, StockTransfer, TransactionType, TransferStatus
from app.models.procurement.procurement import POStatus, PurchaseOrder, PurchaseOrderItem
from app.models.product.product import Product
from app.models.supplier.supplier import Supplier
from app.models.warehouse.warehouse import Warehouse

logger = get_logger(__name__)

SCENARIO_EVENTS = {
    "normal": ["customer_order"] * 3 + ["inventory_movement"] * 2 + ["purchase_request"] + ["warehouse_transfer"],
    "peak_season": ["customer_order"] * 5 + ["demand_spike"] * 2 + ["purchase_request"] * 2 + ["inventory_movement"],
    "supplier_crisis": ["supplier_delay"] * 3 + ["customer_order"] * 2 + ["stockout_risk"] * 2 + ["emergency_purchase"],
    "demand_explosion": ["customer_order"] * 6 + ["demand_spike"] * 3 + ["stockout_risk"] * 2 + ["emergency_purchase"],
    "logistics_crisis": ["warehouse_transfer"] * 3 + ["supplier_delay"] * 2 + ["damage_event"] * 2 + ["stockout_risk"],
    "demand_collapse": ["inventory_movement"] * 3 + ["price_change"] * 2 + ["return_event"] * 2,
    "warehouse_expansion": ["goods_received"] * 3 + ["warehouse_transfer"] * 2 + ["inventory_movement"] * 2,
    "product_recall": ["return_event"] * 3 + ["damage_event"] * 2 + ["adjustment_event"] * 2,
    "import_delay": ["supplier_delay"] * 4 + ["emergency_purchase"] * 3 + ["stockout_risk"] * 2,
    "pandemic": ["demand_spike"] * 2 + ["supplier_delay"] * 3 + ["demand_collapse"] + ["emergency_purchase"] * 2 + ["stockout_risk"],
    "random_chaos": ["customer_order", "supplier_delay", "damage_event", "demand_spike",
                      "return_event", "emergency_purchase", "stockout_risk", "price_change",
                      "adjustment_event", "goods_received"],
}

ALL_SCENARIOS = list(SCENARIO_EVENTS.keys())


class SimulationState:
    def __init__(self):
        self.running = False
        self.paused = False
        self.speed = 1.0
        self.scenario = "normal"
        self.total_events = 0
        self.event_log: list[dict] = []
        self.random_seed: int | None = None


class SimulationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.state = SimulationState()
        from app.services.inventory_service import InventoryService
        self.inventory_svc = InventoryService(db)

    async def generate_business_event(self) -> dict | None:
        if not self.state.running or self.state.paused:
            return None
        events = SCENARIO_EVENTS.get(self.state.scenario, SCENARIO_EVENTS["normal"])
        chosen = random.choice(events)
        return await self._execute_event(chosen)

    async def _execute_event(self, event_type: str) -> dict:
        result = {"type": event_type, "timestamp": datetime.now(timezone.utc).isoformat()}
        try:
            handler = getattr(self, f"_handle_{event_type}", None)
            if handler:
                result.update(await handler())
            else:
                result["error"] = f"No handler for {event_type}"
        except Exception as e:
            logger.warning(f"Simulation event failed: {e}")
            result["error"] = str(e)

        self.state.total_events += 1
        self.state.event_log.append(result)
        if len(self.state.event_log) > 100:
            self.state.event_log.pop(0)
        return result

    async def _handle_customer_order(self) -> dict:
        products = (await self.db.execute(
            select(Product).where(Product.is_active).limit(100)
        )).scalars().all()
        if not products:
            return {"description": "No products available"}
        product = random.choice(products)
        qty = random.randint(1, 20)
        inventories = (await self.db.execute(
            select(Inventory).where(Inventory.product_id == product.id, Inventory.available_quantity > 0).limit(10)
        )).scalars().all()
        if inventories:
            inv = random.choice(inventories)
            await self.inventory_svc.create_transaction(
                inventory_id=inv.id, transaction_type=TransactionType.SALE,
                quantity_change=-min(qty, inv.available_quantity),
                reason=f"Simulated order - {qty} units of {product.name}",
            )
            return {"description": f"Customer ordered {qty} units of {product.name}", "product": product.name}
        return {"description": f"No stock for {product.name}"}

    async def _handle_inventory_movement(self) -> dict:
        inventories = (await self.db.execute(
            select(Inventory).where(Inventory.available_quantity > 0).limit(50)
        )).scalars().all()
        if not inventories:
            return {"description": "No inventory"}
        inv = random.choice(inventories)
        return {"description": f"Cycle count: product at {inv.available_quantity} units in warehouse", "ok": True}

    async def _handle_purchase_request(self) -> dict:
        products = (await self.db.execute(
            select(Product).where(Product.is_active, Product.reorder_level.is_not(None)).limit(50)
        )).scalars().all()
        if not products:
            return {"description": "No products with reorder levels"}
        product = random.choice(products)
        inventories = (await self.db.execute(
            select(Inventory).where(Inventory.product_id == product.id,
                                     Inventory.available_quantity <= (product.reorder_level or 0)).limit(5)
        )).scalars().all()
        if inventories:
            inv = random.choice(inventories)
            return {"description": f"Low stock alert: {product.name} at {inv.available_quantity} (reorder: {product.reorder_level})"}
        return {"description": f"Stock check for {product.name}: adequate"}

    async def _handle_warehouse_transfer(self) -> dict:
        warehouses = (await self.db.execute(select(Warehouse).limit(10))).scalars().all()
        if len(warehouses) < 2:
            return {"description": "Need 2+ warehouses for transfers"}
        from_wh, to_wh = random.sample(warehouses, 2)
        inventories = (await self.db.execute(
            select(Inventory).where(Inventory.warehouse_id == from_wh.id, Inventory.available_quantity > 5).limit(10)
        )).scalars().all()
        if inventories:
            try:
                transfer = StockTransfer(
                    transfer_number=f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100, 999)}",
                    from_warehouse_id=from_wh.id, to_warehouse_id=to_wh.id,
                    status=TransferStatus.DRAFT, notes="Simulated transfer"
                )
                self.db.add(transfer)
                await self.db.flush()
                return {"description": f"Transfer from {from_wh.name} to {to_wh.name}", "transfer_id": str(transfer.id)}
            except Exception as e:
                return {"description": f"Transfer creation failed: {e}"}
        return {"description": f"No inventory to transfer from {from_wh.name}"}

    async def _handle_supplier_delay(self) -> dict:
        suppliers = (await self.db.execute(select(Supplier).limit(20))).scalars().all()
        if not suppliers:
            return {"description": "No suppliers"}
        supplier = random.choice(suppliers)
        days = random.randint(2, 10)
        return {"description": f"Supplier {supplier.legal_name} delayed by {days} days"}

    async def _handle_demand_spike(self) -> dict:
        products = (await self.db.execute(
            select(Product).where(Product.is_active).limit(50)
        )).scalars().all()
        if not products:
            return {"description": "No products"}
        product = random.choice(products)
        pct = random.randint(50, 200)
        return {"description": f"Demand spike: {product.name} orders up {pct}%"}

    async def _handle_stockout_risk(self) -> dict:
        inventories = (await self.db.execute(
            select(Inventory).where(Inventory.available_quantity.between(1, 50)).limit(30)
        )).scalars().all()
        if not inventories:
            return {"description": "No at-risk inventory"}
        inv = random.choice(inventories)
        return {"description": f"Stockout risk: inventory at {inv.available_quantity} units"}

    async def _handle_emergency_purchase(self) -> dict:
        products = (await self.db.execute(
            select(Product).where(Product.is_active).limit(20)
        )).scalars().all()
        if not products:
            return {"description": "No products"}
        product = random.choice(products)
        return {"description": f"Emergency purchase triggered for {product.name}"}

    async def _handle_damage_event(self) -> dict:
        inventories = (await self.db.execute(
            select(Inventory).where(Inventory.available_quantity > 0).limit(50)
        )).scalars().all()
        if not inventories:
            return {"description": "No inventory to damage"}
        inv = random.choice(inventories)
        qty = random.randint(1, min(5, inv.available_quantity))
        try:
            await self.inventory_svc.create_transaction(
                inventory_id=inv.id, transaction_type=TransactionType.DAMAGE,
                quantity_change=-qty, reason="Simulated damage event",
            )
            return {"description": f"Damage: {qty} units lost"}
        except Exception as e:
            return {"description": f"Damage event failed: {e}"}

    async def _handle_return_event(self) -> dict:
        inventories = (await self.db.execute(
            select(Inventory).limit(30)
        )).scalars().all()
        if not inventories:
            return {"description": "No inventory"}
        inv = random.choice(inventories)
        qty = random.randint(1, 10)
        try:
            await self.inventory_svc.create_transaction(
                inventory_id=inv.id, transaction_type=TransactionType.RETURN,
                quantity_change=qty, reason="Simulated customer return",
            )
            return {"description": f"Return received: {qty} units"}
        except Exception as e:
            return {"description": f"Return event failed: {e}"}

    async def _handle_goods_received(self) -> dict:
        pos = (await self.db.execute(
            select(PurchaseOrder).where(
                PurchaseOrder.status.in_([POStatus.APPROVED, POStatus.SENT, POStatus.PARTIALLY_RECEIVED])
            ).limit(10)
        )).scalars().all()
        if not pos:
            return {"description": "No pending POs to receive"}
        po = random.choice(pos)
        items = (await self.db.execute(
            select(PurchaseOrderItem).where(PurchaseOrderItem.purchase_order_id == po.id)
        )).scalars().all()
        if items:
            item = random.choice(items)
            qty = min(random.randint(10, 100), item.quantity - item.received_quantity)
            if qty > 0:
                item.received_quantity += qty
                if item.received_quantity >= item.quantity:
                    po.status = POStatus.RECEIVED
                else:
                    po.status = POStatus.PARTIALLY_RECEIVED
                await self.db.flush()
                return {"description": f"GRN: Received {qty} units against PO {po.po_number}"}
        return {"description": f"No receivable items on PO {po.po_number}"}

    async def _handle_adjustment_event(self) -> dict:
        inventories = (await self.db.execute(
            select(Inventory).limit(50)
        )).scalars().all()
        if not inventories:
            return {"description": "No inventory to adjust"}
        inv = random.choice(inventories)
        return {"description": f"Stock adjustment recorded for inventory {inv.id}"}

    async def _handle_price_change(self) -> dict:
        products = (await self.db.execute(
            select(Product).where(Product.is_active).limit(30)
        )).scalars().all()
        if not products:
            return {"description": "No products"}
        product = random.choice(products)
        pct = random.uniform(-10, 20)
        new_price = float(product.selling_price) * (1 + pct / 100)
        return {"description": f"Price change: {product.name} adjusted by {pct:+.1f}% (new: ₹{new_price:,.0f})"}

    async def generate_seed_data(self) -> dict:
        """Generate realistic seed data through business services."""
        counts = {"products": 0, "suppliers": 0, "warehouses": 0, "inventory": 0}

        # Create warehouses if none exist
        wh_count = (await self.db.execute(select(func.count(Warehouse.id)))).scalar()
        if wh_count == 0:
            cities = [("MUM", "Mumbai"), ("DEL", "Delhi"), ("BLR", "Bangalore"),
                       ("CHE", "Chennai"), ("HYD", "Hyderabad"), ("AHM", "Ahmedabad"), ("PUN", "Pune")]
            for code, city in cities:
                wh = Warehouse(code=f"WH-{code}", name=f"{city} Distribution Center",
                               city=city, country="India", warehouse_type="Distribution")
                self.db.add(wh)
            await self.db.flush()
            counts["warehouses"] = 7

        # Create suppliers if none
        sup_count = (await self.db.execute(select(func.count(Supplier.id)))).scalar()
        if sup_count == 0:
            supplier_names = ["MedSupply Inc", "DentalPro Ltd", "Surgical Solutions", "PharmaDirect",
                              "LabEquip Co", "BioMed Supplies", "HealthCare Distributors", "MediCorp",
                              "Clinical Essentials", "Prime Medical"]
            for i, name in enumerate(supplier_names):
                sup = Supplier(code=f"SUP-{i+1:04d}", legal_name=name,
                               email=f"{name.lower().replace(' ', '')}@example.com",
                               country="India", currency="INR")
                self.db.add(sup)
            await self.db.flush()
            counts["suppliers"] = 10

        # Create a few demo products if none
        prod_count = (await self.db.execute(select(func.count(Product.id)))).scalar()
        if prod_count == 0:
            demo_products = [
                ("SKU-001", "Surgical Mask 3-Ply", 50, 150, 100),
                ("SKU-002", "Nitrile Gloves Large", 200, 600, 400),
                ("SKU-003", "Hand Sanitizer 500ml", 80, 200, 150),
                ("SKU-004", "Digital Thermometer", 150, 450, 300),
                ("SKU-005", "Cotton Bandage Roll", 30, 90, 60),
            ]
            for sku, name, cost, sell, reorder in demo_products:
                p = Product(sku=sku, name=name, cost_price=cost, selling_price=sell,
                            reorder_level=reorder, safety_stock=reorder // 2, is_active=True)
                self.db.add(p)
            await self.db.flush()
            counts["products"] = 5

        await self.db.commit()
        return {"description": "Seed data generated", "counts": counts}
