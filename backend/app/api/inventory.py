import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.providers import get_db
from app.middleware.auth import RequirePermission
from app.models.identity.user import User
from app.repositories.base import PaginationParams
from app.schemas.common import StandardResponse
from app.services.inventory_service import (
    AdjustmentService,
    InventoryService,
    TransferService,
    WarehouseService,
)

router = APIRouter()


# Warehouse endpoints
@router.get("/warehouses")
async def list_warehouses(
    _: User = Depends(RequirePermission("Warehouses.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = WarehouseService(db)
    whs = await svc.list_warehouses()
    return StandardResponse.ok(data=[
        {"id": str(w.id), "code": w.code, "name": w.name, "city": w.city,
         "country": w.country, "warehouse_type": w.warehouse_type, "is_active": w.is_active}
        for w in whs
    ])


@router.post("/warehouses")
async def create_warehouse(
    body: dict,
    _: User = Depends(RequirePermission("Warehouses.Write")),
    db: AsyncSession = Depends(get_db),
):
    svc = WarehouseService(db)
    wh = await svc.create_warehouse(body)
    return StandardResponse.ok(data={"id": str(wh.id)}, message="Warehouse created")


@router.get("/warehouses/{warehouse_id}/zones")
async def list_zones(warehouse_id: uuid.UUID,
    _: User = Depends(RequirePermission("Warehouses.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = WarehouseService(db)
    zones = await svc.list_zones(warehouse_id)
    return StandardResponse.ok(data=[
        {"id": str(z.id), "name": z.name, "code": z.code, "zone_type": z.zone_type}
        for z in zones
    ])


# Inventory endpoints
@router.get("/inventory")
async def list_inventory(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    _: User = Depends(RequirePermission("Inventory.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = InventoryService(db)
    result = await svc.list_inventory(pagination=PaginationParams(page=page, page_size=page_size))
    return StandardResponse.paginated(
        data=[{"id": str(i.id), "product_id": str(i.product_id),
               "warehouse_id": str(i.warehouse_id),
               "available_quantity": i.available_quantity,
               "reserved_quantity": i.reserved_quantity,
               "lot_number": i.lot_number, "expiry_date": str(i.expiry_date) if i.expiry_date else None}
              for i in result.items],
        pagination=result,
    )


@router.get("/inventory/alerts/low-stock")
async def low_stock(
    warehouse_id: uuid.UUID | None = Query(None),
    _: User = Depends(RequirePermission("Inventory.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = InventoryService(db)
    items = await svc.get_low_stock(warehouse_id)
    return StandardResponse.ok(data=[
        {"id": str(i.id), "product_id": str(i.product_id),
         "available": i.available_quantity, "reorder_level": i.reorder_level}
        for i in items
    ])


@router.get("/inventory/alerts/expiring")
async def expiring(
    days: int = Query(30),
    _: User = Depends(RequirePermission("Inventory.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = InventoryService(db)
    items = await svc.get_expiring(days)
    return StandardResponse.ok(data=[
        {"id": str(i.id), "product_id": str(i.product_id),
         "expiry_date": str(i.expiry_date), "available_quantity": i.available_quantity}
        for i in items
    ])


@router.get("/inventory/{inventory_id}/transactions")
async def get_transactions(
    inventory_id: uuid.UUID,
    _: User = Depends(RequirePermission("Inventory.ViewHistory")),
    db: AsyncSession = Depends(get_db),
):
    svc = InventoryService(db)
    txns = await svc.get_transaction_history(inventory_id)
    return StandardResponse.ok(data=[
        {"id": str(t.id), "type": t.transaction_type.value,
         "before": t.before_quantity, "after": t.after_quantity,
         "change": t.quantity_change, "reason": t.reason,
         "created_at": t.created_at.isoformat()}
        for t in txns
    ])


@router.post("/transfers")
async def create_transfer(
    body: dict,
    current_user: User = Depends(RequirePermission("Inventory.Transfer")),
    db: AsyncSession = Depends(get_db),
):
    svc = TransferService(db)
    transfer = await svc.create_transfer(body, current_user.id)
    return StandardResponse.ok(data={"id": str(transfer.id)}, message="Transfer created")


@router.post("/adjustments")
async def create_adjustment(
    body: dict,
    current_user: User = Depends(RequirePermission("Inventory.Adjust")),
    db: AsyncSession = Depends(get_db),
):
    svc = AdjustmentService(db)
    adj = await svc.create_adjustment(body, current_user.id)
    return StandardResponse.ok(data={"id": str(adj.id)}, message="Adjustment created")
