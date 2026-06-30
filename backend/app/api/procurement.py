import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.providers import get_db
from app.middleware.auth import get_current_user, RequirePermission
from app.services.procurement_service import ProcurementService, SupplierService
from app.models.identity.user import User
from app.schemas.common import StandardResponse
from app.repositories.base import PaginationParams

router = APIRouter()


# Supplier endpoints
@router.get("/suppliers")
async def list_suppliers(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierService(db)
    result = await svc.list_suppliers(pagination=PaginationParams(page=page, page_size=page_size))
    return StandardResponse.paginated(
        data=[{"id": str(s.id), "code": s.code, "legal_name": s.legal_name,
               "display_name": s.display_name, "gst_number": s.gst_number,
               "country": s.country, "email": s.email, "phone": s.phone,
               "rating": s.rating, "is_active": s.is_active}
              for s in result.items],
        pagination=result,
    )


@router.get("/suppliers/{supplier_id}")
async def get_supplier(
    supplier_id: uuid.UUID,
    _: User = Depends(RequirePermission("Suppliers.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierService(db)
    supplier = await svc.get_supplier(supplier_id)
    return StandardResponse.ok(data={
        "id": str(supplier.id), "code": supplier.code,
        "legal_name": supplier.legal_name, "display_name": supplier.display_name,
        "gst_number": supplier.gst_number, "pan": supplier.pan,
        "email": supplier.email, "phone": supplier.phone,
        "website": supplier.website, "country": supplier.country,
        "state": supplier.state, "city": supplier.city,
        "currency": supplier.currency, "payment_terms": supplier.payment_terms,
        "is_preferred": supplier.is_preferred, "rating": supplier.rating,
        "contacts": [{"id": str(c.id), "name": c.name, "email": c.email, "phone": c.phone,
                       "contact_type": c.contact_type, "is_primary": c.is_primary}
                      for c in supplier.contacts],
        "documents": [{"id": str(d.id), "name": d.name, "document_type": d.document_type}
                      for d in supplier.documents],
    })


@router.post("/suppliers")
async def create_supplier(
    body: dict,
    _: User = Depends(RequirePermission("Suppliers.Create")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierService(db)
    supplier = await svc.create_supplier(body)
    return StandardResponse.ok(data={"id": str(supplier.id)}, message="Supplier created")


@router.put("/suppliers/{supplier_id}")
async def update_supplier(
    supplier_id: uuid.UUID, body: dict,
    _: User = Depends(RequirePermission("Suppliers.Update")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierService(db)
    supplier = await svc.update_supplier(supplier_id, body)
    return StandardResponse.ok(data={"id": str(supplier.id)}, message="Supplier updated")


# Purchase Order endpoints
@router.get("/purchase-orders")
async def list_purchase_orders(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    _: User = Depends(RequirePermission("PurchaseOrders.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = ProcurementService(db)
    result = await svc.list_purchase_orders(pagination=PaginationParams(page=page, page_size=page_size))
    return StandardResponse.paginated(
        data=[{"id": str(po.id), "po_number": po.po_number,
               "supplier_id": str(po.supplier_id), "warehouse_id": str(po.warehouse_id),
               "status": po.status.value, "total_amount": float(po.total_amount),
               "expected_delivery_date": str(po.expected_delivery_date) if po.expected_delivery_date else None,
               "created_at": po.created_at.isoformat()}
              for po in result.items],
        pagination=result,
    )


@router.get("/purchase-orders/{po_id}")
async def get_purchase_order(
    po_id: uuid.UUID,
    _: User = Depends(RequirePermission("PurchaseOrders.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = ProcurementService(db)
    po = await svc.get_purchase_order(po_id)
    return StandardResponse.ok(data={
        "id": str(po.id), "po_number": po.po_number,
        "supplier_id": str(po.supplier_id), "warehouse_id": str(po.warehouse_id),
        "status": po.status.value, "subtotal": float(po.subtotal),
        "tax_amount": float(po.tax_amount), "total_amount": float(po.total_amount),
        "currency": po.currency, "notes": po.notes,
        "expected_delivery_date": str(po.expected_delivery_date) if po.expected_delivery_date else None,
        "items": [{"id": str(i.id), "product_id": str(i.product_id),
                    "quantity": i.quantity, "received_quantity": i.received_quantity,
                    "unit_cost": float(i.unit_cost), "line_total": float(i.line_total)}
                   for i in po.items],
        "approvals": [{"approver_id": str(a.approver_id), "status": a.status,
                        "notes": a.notes, "decided_at": a.decided_at.isoformat() if a.decided_at else None}
                       for a in po.approvals],
        "created_at": po.created_at.isoformat(),
    })


@router.post("/purchase-orders")
async def create_purchase_order(
    body: dict,
    current_user: User = Depends(RequirePermission("PurchaseOrders.Create")),
    db: AsyncSession = Depends(get_db),
):
    svc = ProcurementService(db)
    po = await svc.create_purchase_order(body, current_user.id)
    return StandardResponse.ok(data={"id": str(po.id), "po_number": po.po_number}, message="PO created")


@router.post("/purchase-orders/{po_id}/approve")
async def approve_po(
    po_id: uuid.UUID, body: dict,
    current_user: User = Depends(RequirePermission("PurchaseOrders.Approve")),
    db: AsyncSession = Depends(get_db),
):
    svc = ProcurementService(db)
    await svc.approve_po(po_id, current_user.id, body.get("notes"))
    return StandardResponse.ok(message="Purchase order approved")


@router.post("/grn")
async def create_grn(
    body: dict,
    current_user: User = Depends(RequirePermission("PurchaseOrders.Receive")),
    db: AsyncSession = Depends(get_db),
):
    svc = ProcurementService(db)
    grn = await svc.receive_goods(uuid.UUID(body["purchase_order_id"]), body, current_user.id)
    return StandardResponse.ok(data={"id": str(grn.id), "grn_number": grn.grn_number}, message="GRN created")
