"""Supplier Intelligence API — comparison, scorecards, risk, recommendations, quotation analysis."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.providers import get_db
from app.middleware.auth import RequirePermission
from app.models.identity.user import User
from app.schemas.common import StandardResponse
from app.services.supplier_intelligence_service import SupplierIntelligenceService

router = APIRouter()


@router.get("/suppliers/{supplier_id}/dashboard")
async def supplier_dashboard(
    supplier_id: uuid.UUID,
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierIntelligenceService(db)
    data = await svc.get_dashboard(supplier_id)
    return StandardResponse.ok(data=data)


@router.post("/suppliers/compare")
async def compare_suppliers(
    body: dict,
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    ids = [uuid.UUID(i) for i in body.get("supplier_ids", [])]
    svc = SupplierIntelligenceService(db)
    data = await svc.compare_suppliers(ids)
    return StandardResponse.ok(data=data)


@router.get("/suppliers/{supplier_id}/scorecard")
async def supplier_scorecard(
    supplier_id: uuid.UUID,
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierIntelligenceService(db)
    data = await svc.get_scorecard(supplier_id)
    return StandardResponse.ok(data=data)


@router.get("/suppliers/risks")
async def assess_risks(
    supplier_id: uuid.UUID | None = None,
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierIntelligenceService(db)
    data = await svc.assess_risks(supplier_id)
    return StandardResponse.ok(data=data)


@router.get("/suppliers/{supplier_id}/recommendations")
async def supplier_recommendations(
    supplier_id: uuid.UUID,
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierIntelligenceService(db)
    data = await svc.get_recommendations(supplier_id)
    return StandardResponse.ok(data=data)


@router.post("/suppliers/{supplier_id}/quotation-analysis")
async def analyze_quotation(
    supplier_id: uuid.UUID, body: dict,
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierIntelligenceService(db)
    data = await svc.analyze_quotation(supplier_id, body)
    return StandardResponse.ok(data=data)
