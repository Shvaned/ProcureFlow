import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import BusinessRuleException, ConflictException, NotFoundException
from app.models.procurement.procurement import (
    GoodsReceivedNote,
    POStatus,
    PRStatus,
    PurchaseOrder,
    PurchaseOrderApproval,
    PurchaseOrderItem,
    PurchaseReceipt,
    PurchaseRequest,
)
from app.models.supplier.supplier import Supplier
from app.repositories.base import BaseRepository


class ProcurementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_purchase_request(self, data: dict, user_id: uuid.UUID) -> PurchaseRequest:
        import secrets
        pr = PurchaseRequest(
            pr_number=f"PR-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}",
            warehouse_id=uuid.UUID(data["warehouse_id"]),
            requested_by=user_id,
            notes=data.get("notes"),
            status=PRStatus.DRAFT,
        )
        self.db.add(pr)
        await self.db.flush()
        return pr

    async def create_purchase_order(self, data: dict, user_id: uuid.UUID) -> PurchaseOrder:
        import secrets
        po = PurchaseOrder(
            po_number=f"PO-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}",
            supplier_id=uuid.UUID(data["supplier_id"]),
            warehouse_id=uuid.UUID(data["warehouse_id"]),
            pr_id=uuid.UUID(data["pr_id"]) if data.get("pr_id") else None,
            expected_delivery_date=data.get("expected_delivery_date"),
            currency=data.get("currency", "INR"),
            notes=data.get("notes"),
            status=POStatus.DRAFT,
            created_by=user_id,
        )
        self.db.add(po)
        await self.db.flush()

        subtotal = Decimal("0")
        tax_amount = Decimal("0")
        for item_data in data.get("items", []):
            qty = item_data["quantity"]
            unit_cost = Decimal(str(item_data["unit_cost"]))
            tax_pct = Decimal(str(item_data.get("tax_pct", 0)))
            line_total = unit_cost * qty
            subtotal += line_total
            tax_amount += line_total * (tax_pct / Decimal("100"))

            item = PurchaseOrderItem(
                purchase_order_id=po.id,
                product_id=uuid.UUID(item_data["product_id"]),
                quantity=qty,
                unit_cost=unit_cost,
                discount_pct=Decimal(str(item_data.get("discount_pct", 0))),
                tax_pct=tax_pct,
                line_total=line_total,
                expected_date=item_data.get("expected_date"),
            )
            self.db.add(item)

        po.subtotal = subtotal
        po.tax_amount = tax_amount
        po.total_amount = subtotal + tax_amount + Decimal(str(data.get("shipping_amount", 0)))
        await self.db.flush()
        return po

    async def get_purchase_order(self, po_id: uuid.UUID) -> PurchaseOrder:
        result = await self.db.execute(
            select(PurchaseOrder).where(PurchaseOrder.id == po_id).options(
                selectinload(PurchaseOrder.items),
                selectinload(PurchaseOrder.approvals),
            )
        )
        po = result.scalar_one_or_none()
        if not po:
            raise NotFoundException("Purchase order not found")
        return po

    async def list_purchase_orders(self, filters=None, sorting=None, pagination=None):
        repo = BaseRepository[PurchaseOrder](self.db)
        repo.model = PurchaseOrder
        return await repo.find_all(filters, sorting, pagination)

    async def approve_po(self, po_id: uuid.UUID, approver_id: uuid.UUID, notes: str | None = None):
        po = await self.get_purchase_order(po_id)
        if po.status != POStatus.DRAFT:
            raise BusinessRuleException("Only draft purchase orders can be approved")

        approval = PurchaseOrderApproval(
            purchase_order_id=po_id, approver_id=approver_id,
            approval_level=1, status="approved", notes=notes,
            decided_at=datetime.now(timezone.utc),
        )
        self.db.add(approval)
        po.status = POStatus.APPROVED
        po.approved_by = approver_id
        po.approved_at = datetime.now(timezone.utc)
        await self.db.flush()

    async def receive_goods(self, po_id: uuid.UUID, data: dict, user_id: uuid.UUID) -> GoodsReceivedNote:
        import secrets
        po = await self.get_purchase_order(po_id)
        if po.status not in (POStatus.APPROVED, POStatus.SENT, POStatus.PARTIALLY_RECEIVED):
            raise BusinessRuleException("PO must be approved before receiving goods")

        grn = GoodsReceivedNote(
            grn_number=f"GRN-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}",
            purchase_order_id=po_id,
            warehouse_id=po.warehouse_id,
            received_by=user_id,
            received_date=data.get("received_date", date.today()),
            notes=data.get("notes"),
        )
        self.db.add(grn)

        for item_data in data.get("items", []):
            receipt = PurchaseReceipt(
                purchase_order_id=po_id, grn_id=grn.id,
                product_id=uuid.UUID(item_data["product_id"]),
                received_quantity=item_data["received_quantity"],
                accepted_quantity=item_data.get("accepted_quantity", item_data["received_quantity"]),
                rejected_quantity=item_data.get("rejected_quantity", 0),
                damaged_quantity=item_data.get("damaged_quantity", 0),
                lot_number=item_data.get("lot_number"),
                batch_number=item_data.get("batch_number"),
                expiry_date=item_data.get("expiry_date"),
                condition=item_data.get("condition", "Good"),
            )
            self.db.add(receipt)

        po.status = POStatus.PARTIALLY_RECEIVED
        await self.db.flush()
        return grn


class SupplierService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_suppliers(self, filters=None, sorting=None, pagination=None):
        repo = BaseRepository[Supplier](self.db)
        repo.model = Supplier
        return await repo.find_all(filters, sorting, pagination)

    async def get_supplier(self, supplier_id: uuid.UUID) -> Supplier:
        result = await self.db.execute(
            select(Supplier).where(Supplier.id == supplier_id).options(
                selectinload(Supplier.contacts),
                selectinload(Supplier.documents),
                selectinload(Supplier.performance),
            )
        )
        supplier = result.scalar_one_or_none()
        if not supplier:
            raise NotFoundException("Supplier not found")
        return supplier

    async def create_supplier(self, data: dict) -> Supplier:
        repo = BaseRepository[Supplier](self.db)
        repo.model = Supplier
        if data.get("gst_number"):
            existing = await self.db.execute(
                select(Supplier).where(Supplier.gst_number == data["gst_number"])
            )
            if existing.scalar_one_or_none():
                raise ConflictException("Supplier with this GST number already exists")

        supplier = Supplier(
            code=data["code"], legal_name=data["legal_name"],
            display_name=data.get("display_name"), gst_number=data.get("gst_number"),
            pan=data.get("pan"), email=data.get("email"),
            phone=data.get("phone"), website=data.get("website"),
            country=data.get("country"), state=data.get("state"),
            city=data.get("city"), currency=data.get("currency", "INR"),
            payment_terms=data.get("payment_terms"),
        )
        return await repo.create(supplier)

    async def update_supplier(self, supplier_id: uuid.UUID, data: dict) -> Supplier:
        supplier = await self.get_supplier(supplier_id)
        updatable = ["display_name", "email", "phone", "website", "country",
                      "state", "city", "currency", "payment_terms", "is_active", "notes"]
        for field in updatable:
            if field in data:
                setattr(supplier, field, data[field])
        repo = BaseRepository[Supplier](self.db)
        repo.model = Supplier
        return await repo.update(supplier)
