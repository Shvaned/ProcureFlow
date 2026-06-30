"""Supplier Intelligence — comparison, scoring, risk, recommendations."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.procurement.procurement import POStatus, PurchaseOrder
from app.models.supplier.supplier import Supplier, SupplierPerformance


class SupplierIntelligenceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard(self, supplier_id: uuid.UUID) -> dict:
        supplier = await self._get_supplier(supplier_id)
        perf = await self._get_performance(supplier_id)
        pos = await self._get_supplier_pos(supplier_id)

        return {
            "supplier": {
                "id": str(supplier.id), "code": supplier.code, "legal_name": supplier.legal_name,
                "email": supplier.email, "country": supplier.country,
                "rating": supplier.rating, "is_preferred": supplier.is_preferred,
                "is_active": supplier.is_active,
            },
            "performance": perf,
            "procurement": {
                "total_pos": len(pos), "open_pos": len([p for p in pos if p.status in (POStatus.APPROVED, POStatus.SENT, POStatus.PARTIALLY_RECEIVED)]),
                "total_spend": float(sum((p.total_amount or 0) for p in pos)),
                "recent_pos": [{"po_number": p.po_number, "status": p.status.value, "total": float(p.total_amount), "date": p.created_at.isoformat()} for p in pos[:5]],
            },
            "risk_level": self._assess_risk_level(supplier, perf, pos),
            "scorecard": await self.get_scorecard(supplier_id),
        }

    async def compare_suppliers(self, supplier_ids: list[uuid.UUID]) -> dict:
        results = []
        for sid in supplier_ids:
            try:
                supplier = await self._get_supplier(sid)
                perf = await self._get_performance(sid)
                results.append({
                    "id": str(supplier.id), "name": supplier.legal_name,
                    "rating": supplier.rating, "country": supplier.country,
                    "is_preferred": supplier.is_preferred,
                    "lead_time": perf.get("avg_lead_time_days"),
                    "quality": perf.get("quality_rating"),
                    "delivery": perf.get("delivery_rating"),
                    "on_time_pct": perf.get("on_time_delivery_pct"),
                    "overall_score": perf.get("overall_score"),
                })
            except Exception:
                continue

        # Rank by overall score descending
        results.sort(key=lambda r: r.get("overall_score") or 0, reverse=True)
        recommendation = ""
        if results:
            top = results[0]
            recommendation = f"Recommended: {top['name']} (overall score: {top.get('overall_score', 0):.1f}/5.0)"

        return {
            "suppliers": results,
            "count": len(results),
            "recommendation": recommendation,
        }

    async def get_scorecard(self, supplier_id: uuid.UUID) -> dict:
        perf = await self._get_performance(supplier_id)
        ratings = {
            "on_time_delivery": perf.get("on_time_delivery_pct", 0),
            "quality_score": perf.get("quality_rating", 0),
            "delivery_rating": perf.get("delivery_rating", 0),
            "price_competitiveness": perf.get("price_competitiveness", 0),
            "overall_score": perf.get("overall_score", 0),
        }
        # Letter grade based on overall score
        overall = ratings["overall_score"]
        grade = "A" if overall >= 4.5 else "B" if overall >= 3.5 else "C" if overall >= 2.5 else "D"

        return {"supplier_id": str(supplier_id), "ratings": ratings, "grade": grade,
                "summary": f"Overall rating: {overall:.1f}/5.0 (Grade {grade})"}

    async def assess_risks(self, supplier_id: uuid.UUID | None = None) -> list[dict]:
        risks = []
        # Check for single-source dependencies
        if supplier_id:
            supplier = await self._get_supplier(supplier_id)
            perf = await self._get_performance(supplier_id)
            if perf.get("on_time_delivery_pct", 100) < 80:
                risks.append({"type": "delivery_risk", "severity": "high",
                               "description": f"On-time delivery below 80% for {supplier.legal_name}",
                               "mitigation": "Consider backup suppliers or negotiate delivery terms"})
            if perf.get("quality_rating", 5) < 3.0:
                risks.append({"type": "quality_risk", "severity": "high",
                               "description": f"Quality rating below 3.0 for {supplier.legal_name}",
                               "mitigation": "Implement quality inspection at receiving"})
            if supplier.rating < 2.5:
                risks.append({"type": "performance_risk", "severity": "medium",
                               "description": f"Low overall rating ({supplier.rating})",
                               "mitigation": "Review supplier relationship and set improvement targets"})
        else:
            # Global risk scan
            suppliers = (await self.db.execute(select(Supplier).where(Supplier.is_active))).scalars().all()
            for s in suppliers:
                perf = await self._get_performance(s.id)
                if perf.get("on_time_delivery_pct", 100) < 70:
                    risks.append({"type": "delivery_risk", "severity": "high", "supplier": s.legal_name,
                                   "description": f"{s.legal_name}: {perf['on_time_delivery_pct']}% on-time delivery"})

        if not risks:
            risks.append({"type": "none", "severity": "low", "description": "No significant risks detected"})
        return risks

    async def get_recommendations(self, supplier_id: uuid.UUID) -> dict:
        supplier = await self._get_supplier(supplier_id)
        perf = await self._get_performance(supplier_id)
        pos = await self._get_supplier_pos(supplier_id)

        recommendations = []
        if supplier.is_preferred and supplier.rating >= 4.0:
            recommendations.append({"action": "Increase order volume", "reason": "High-performing preferred supplier",
                                     "savings_estimate": "Potential 5-10% cost savings through consolidation"})
        if perf.get("lead_time_days", 0) > 7:
            recommendations.append({"action": "Negotiate shorter lead times", "reason": f"Current: {perf['lead_time_days']} days",
                                     "savings_estimate": "Reduced inventory holding costs"})
        if len(pos) > 5:
            recommendations.append({"action": "Consider volume discount negotiation", "reason": f"{len(pos)} POs placed",
                                     "savings_estimate": "3-8% through bulk purchasing"})

        return {
            "supplier_name": supplier.legal_name,
            "recommendations": recommendations,
            "priority_actions": [r["action"] for r in recommendations[:2]],
        }

    async def analyze_quotation(self, supplier_id: uuid.UUID, quotation_data: dict) -> dict:
        """Analyze a supplier quotation against historical data."""
        supplier = await self._get_supplier(supplier_id)
        perf = await self._get_performance(supplier_id)

        items = quotation_data.get("items", [])
        total_quoted = sum(
            float(i.get("unit_price", 0)) * int(i.get("quantity", 0)) for i in items
        )

        return {
            "supplier_name": supplier.legal_name,
            "quoted_total": total_quoted,
            "supplier_rating": supplier.rating,
            "on_time_pct": perf.get("on_time_delivery_pct", 0),
            "avg_lead_time": perf.get("avg_lead_time_days"),
            "recommendation": "Accept quotation" if supplier.rating >= 3.5 and perf.get("on_time_delivery_pct", 0) >= 80 else "Review carefully",
            "confidence": round(supplier.rating * 20, 0),
            "risks": ["Above average lead time"] if (perf.get("avg_lead_time_days") or 0) > 10 else [],
        }

    async def _get_supplier(self, sid: uuid.UUID) -> Supplier:
        result = await self.db.execute(select(Supplier).where(Supplier.id == sid))
        s = result.scalar_one_or_none()
        if not s:
            raise NotFoundException("Supplier not found")
        return s

    async def _get_performance(self, sid: uuid.UUID) -> dict:
        result = await self.db.execute(
            select(SupplierPerformance).where(SupplierPerformance.supplier_id == sid)
        )
        p = result.scalar_one_or_none()
        if not p:
            return {}
        return {
            "avg_lead_time_days": p.avg_lead_time_days,
            "late_deliveries_count": p.late_deliveries_count,
            "rejected_goods_count": p.rejected_goods_count,
            "quality_rating": p.quality_rating,
            "delivery_rating": p.delivery_rating,
            "price_competitiveness": p.price_competitiveness,
            "overall_score": p.overall_score,
            "on_time_delivery_pct": p.on_time_delivery_pct,
            "total_purchase_orders": p.total_purchase_orders,
        }

    async def _get_supplier_pos(self, sid: uuid.UUID) -> list[PurchaseOrder]:
        result = await self.db.execute(
            select(PurchaseOrder).where(PurchaseOrder.supplier_id == sid)
            .order_by(PurchaseOrder.created_at.desc()).limit(20)
        )
        return list(result.scalars().all())

    def _assess_risk_level(self, supplier: Supplier, perf: dict, pos: list) -> str:
        score = 0
        if perf.get("on_time_delivery_pct", 100) < 80:
            score += 1
        if perf.get("quality_rating", 5) < 3.0:
            score += 1
        if supplier.rating < 1.5:
            score += 1
        if perf.get("late_deliveries_count", 0) > 5:
            score += 1
        if score >= 3:
            return "critical"
        if score >= 2:
            return "high"
        if score >= 1:
            return "medium"
        return "low"
