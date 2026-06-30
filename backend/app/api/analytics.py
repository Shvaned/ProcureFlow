import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.providers import get_db
from app.middleware.auth import get_current_user, RequirePermission
from app.services.analytics_service import AnalyticsService
from app.models.identity.user import User
from app.schemas.common import StandardResponse

router = APIRouter()


@router.get("/analytics/executive")
async def executive_summary(
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_executive_summary()
    return StandardResponse.ok(data=data)


@router.get("/analytics/inventory")
async def inventory_analytics(
    warehouse_id: uuid.UUID | None = Query(None),
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_inventory_analytics(warehouse_id)
    return StandardResponse.ok(data=data)


@router.get("/analytics/low-stock")
async def low_stock_summary(
    warehouse_id: uuid.UUID | None = Query(None),
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_low_stock_summary(warehouse_id)
    return StandardResponse.ok(data=data)


@router.get("/analytics/supplier")
async def supplier_analytics(
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_supplier_analytics()
    return StandardResponse.ok(data=data)


@router.get("/analytics/procurement")
async def procurement_analytics(
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_procurement_analytics()
    return StandardResponse.ok(data=data)


@router.get("/analytics/warehouse")
async def warehouse_analytics(
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_warehouse_analytics()
    return StandardResponse.ok(data=data)


@router.get("/analytics/product")
async def product_analytics(
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_product_analytics()
    return StandardResponse.ok(data=data)


@router.get("/kpis/{kpi_key}")
async def get_kpi(
    kpi_key: str,
    _: User = Depends(RequirePermission("Analytics.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = AnalyticsService(db)
    data = await svc.get_kpi_data(kpi_key)
    return StandardResponse.ok(data=data)
