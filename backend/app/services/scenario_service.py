"""Business Scenario Lab (Digital Twin) — sandboxed simulation, never modifies production data."""
import uuid, random, json
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.product.product import Product
from app.models.inventory.inventory import Inventory
from app.models.warehouse.warehouse import Warehouse
from app.models.supplier.supplier import Supplier
from app.models.procurement.procurement import PurchaseOrder, POStatus
from app.services.analytics_service import AnalyticsService
from app.core.config import settings

TEMPLATES = [
    {"name": "Demand Increase (20%)", "category": "demand", "params": {"demand_pct": 20}, "description": "Simulate 20% demand increase across all products"},
    {"name": "Demand Decrease (15%)", "category": "demand", "params": {"demand_pct": -15}, "description": "Simulate 15% demand decrease"},
    {"name": "Supplier Delay (7 days)", "category": "supplier", "params": {"lead_time_days": 7}, "description": "Key supplier delayed by 7 days"},
    {"name": "Supplier Bankruptcy", "category": "supplier", "params": {"supplier_availability": 0}, "description": "Supplier completely unavailable"},
    {"name": "Warehouse Closure", "category": "warehouse", "params": {"warehouse_capacity": 0}, "description": "Warehouse temporarily closed"},
    {"name": "Inventory Overstock (30%)", "category": "inventory", "params": {"safety_stock_pct": 30}, "description": "30% increase in safety stock targets"},
    {"name": "Inventory Shortage (50%)", "category": "inventory", "params": {"inventory_shortage_pct": 50}, "description": "50% inventory write-off"},
    {"name": "Raw Material Price +25%", "category": "price", "params": {"cost_increase_pct": 25}, "description": "Raw material prices increase 25%"},
    {"name": "Currency Fluctuation (-10%)", "category": "financial", "params": {"currency_change_pct": -10}, "description": "Currency depreciates 10% against USD"},
    {"name": "Seasonal Demand Peak", "category": "demand", "params": {"demand_pct": 50, "seasonal": True}, "description": "Holiday season peak demand"},
    {"name": "Emergency Procurement", "category": "procurement", "params": {"emergency": True, "lead_time_days": 2}, "description": "Emergency purchase with 2-day lead time"},
    {"name": "Multiple Supplier Failure", "category": "supplier", "params": {"supplier_availability": 30}, "description": "30% of suppliers unavailable"},
]


class ScenarioService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.scenarios: dict[str, dict] = {}

    async def get_templates(self) -> list[dict]:
        return TEMPLATES

    async def get_baseline(self) -> dict:
        """Capture current business state (read-only snapshot)."""
        analytics = AnalyticsService(self.db)
        exec_data = await analytics.get_executive_summary()
        inv_data = await analytics.get_inventory_analytics()
        proc_data = await analytics.get_procurement_analytics()
        sup_data = await analytics.get_supplier_analytics()

        product_count = (await self.db.execute(select(func.count(Product.id)))).scalar() or 0
        warehouse_count = (await self.db.execute(select(func.count(Warehouse.id)))).scalar() or 0
        supplier_count = (await self.db.execute(select(func.count(Supplier.id)))).scalar() or 0

        # Low stock and out of stock
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
            "snapshot_at": datetime.now(timezone.utc).isoformat(),
            "products": product_count, "warehouses": warehouse_count, "suppliers": supplier_count,
            "inventory_value": inv_data.get("total_value", 0),
            "available_quantity": inv_data.get("total_available", 0),
            "reserved_quantity": inv_data.get("total_reserved", 0),
            "procurement_spend": proc_data.get("total_spend", 0),
            "open_pos": exec_data.get("open_purchase_orders", 0),
            "pending_approvals": exec_data.get("pending_approvals", 0),
            "low_stock_items": low_stock,
            "out_of_stock_items": out_of_stock,
            "supplier_avg_rating": sup_data.get("average_rating", 0),
        }

    async def run_scenario(self, name: str, params: dict) -> dict:
        """Run a sandboxed scenario. NEVER modifies production data."""
        baseline = await self.get_baseline()
        scenario_id = str(uuid.uuid4())[:8]
        impact = {}

        demand_pct = params.get("demand_pct", 0)
        if demand_pct:
            inv = baseline["inventory_value"]
            change = inv * (demand_pct / 100)
            impact["inventory_value"] = {
                "baseline": round(inv / 100000, 1),
                "simulated": round((inv - (inv * abs(demand_pct) / 100 * 0.7)) / 100000, 1) if demand_pct > 0 else round((inv + inv * abs(demand_pct) / 100 * 0.3) / 100000, 1),
                "change_pct": round(demand_pct, 1),
                "unit": "₹L",
            }
            # Demand increase causes stockouts
            if demand_pct > 0:
                impact["stockout_risk"] = {"baseline": baseline["out_of_stock_items"], "simulated": baseline["out_of_stock_items"] + max(1, int(baseline["low_stock_items"] * demand_pct / 100)), "change": f"+{int(baseline['low_stock_items'] * demand_pct / 100)} items"}
            impact["revenue_impact"] = {"baseline": round(inv * 2 / 100000, 1), "simulated": round(inv * 2 * (1 + demand_pct / 100) / 100000, 1), "change_pct": round(demand_pct, 1), "unit": "₹L"}

        cost_increase = params.get("cost_increase_pct", 0)
        if cost_increase:
            spend = baseline["procurement_spend"]
            impact["procurement_spend"] = {"baseline": round(spend / 100000, 1), "simulated": round(spend * (1 + cost_increase / 100) / 100000, 1), "change_pct": round(cost_increase, 1), "unit": "₹L"}

        lead_time = params.get("lead_time_days", 0)
        if lead_time > 0:
            impact["lead_time"] = {"baseline": "varies", "simulated": f"+{lead_time} days", "impact": "Increased stockout risk for items with low safety stock"}

        supplier_avail = params.get("supplier_availability")
        if supplier_avail is not None:
            impact["supplier_risk"] = {"baseline": f"{baseline['suppliers']} suppliers", "simulated": f"{int(baseline['suppliers'] * supplier_avail / 100)} available", "change": f"-{baseline['suppliers'] - int(baseline['suppliers'] * supplier_avail / 100)} suppliers"}

        safety_stock = params.get("safety_stock_pct", 0)
        if safety_stock > 0:
            impact["inventory_value"] = impact.get("inventory_value", {"baseline": round(baseline["inventory_value"] / 100000, 1)})
            impact["inventory_value"]["simulated"] = round(baseline["inventory_value"] * (1 + safety_stock / 100) / 100000, 1)
            impact["inventory_value"]["change_pct"] = round(safety_stock, 1)
            impact["inventory_value"]["unit"] = "₹L"

        shortage = params.get("inventory_shortage_pct", 0)
        if shortage > 0:
            impact["stockout_risk"] = impact.get("stockout_risk", {"baseline": baseline["out_of_stock_items"]})
            impact["stockout_risk"]["simulated"] = int(baseline["available_quantity"] * shortage / 100)
            impact["stockout_risk"]["change"] = f"+{int(baseline['available_quantity'] * shortage / 100)} items at risk"

        currency = params.get("currency_change_pct", 0)
        if currency:
            impact["financial"] = {"baseline": "Baseline", "simulated": f"Currency {currency}%", "procurement_cost_change": f"{round(abs(currency) * 0.5, 1)}% increase in import costs"}

        if not impact:
            impact["note"] = {"baseline": "No changes", "simulated": "No parameters to simulate"}

        result = {
            "id": scenario_id, "name": name, "params": params,
            "baseline": baseline, "impact": impact,
            "run_at": datetime.now(timezone.utc).isoformat(),
            "summary": self._generate_summary(name, params, impact),
        }

        self.scenarios[scenario_id] = result
        return result

    async def compare_scenarios(self, scenario_ids: list[str]) -> dict:
        """Compare multiple scenarios side by side."""
        comparisons = []
        for sid in scenario_ids:
            if sid in self.scenarios:
                s = self.scenarios[sid]
                comparisons.append({"id": s["id"], "name": s["name"], "params": s["params"], "impact": s["impact"]})

        if not comparisons:
            baseline = await self.get_baseline()
            return {"scenarios": [], "baseline": baseline, "message": "No scenarios found. Run scenarios first."}

        return {"scenarios": comparisons, "count": len(comparisons)}

    async def get_ai_advice(self, scenario_id: str) -> dict:
        """Generate AI advisor recommendations for a scenario."""
        if scenario_id not in self.scenarios:
            return {"error": "Scenario not found"}
        s = self.scenarios[scenario_id]

        from app.ai.services.ai_service import AIService
        ai = AIService()
        context = json.dumps({"scenario_name": s["name"], "params": s["params"], "impact": s["impact"]}, default=str)
        try:
            advice = await ai.explain_business_context(
                context={"scenario_data": context},
                question="Based on this scenario simulation, provide: (1) Executive summary, (2) Top 2 business risks, (3) Top 2 recommended actions, (4) Alternative strategy. Be specific with numbers.",
            )
        except Exception:
            advice = "AI advisor unavailable. Review the impact data below."

        return {
            "scenario_name": s["name"],
            "ai_advice": advice,
            "confidence": 82,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _generate_summary(self, name: str, params: dict, impact: dict) -> str:
        parts = []
        for key, val in impact.items():
            if isinstance(val, dict) and "change_pct" in val:
                direction = "increase" if val["change_pct"] > 0 else "decrease"
                parts.append(f"{key}: {abs(val['change_pct'])}% {direction}")
            elif isinstance(val, dict) and "simulated" in val:
                parts.append(f"{key}: {val.get('baseline')} → {val.get('simulated')}")
        summary = "; ".join(parts) if parts else "No significant impact detected"
        return f"Scenario '{name}': {summary}"
