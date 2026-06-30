import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessRuleException, NotFoundException
from app.models.inventory.inventory import (
    AdjustmentReason,
    Inventory,
    InventoryTransaction,
    StockAdjustment,
    StockTransfer,
    StockTransferItem,
    TransactionType,
    TransferStatus,
)
from app.models.warehouse.warehouse import Warehouse, WarehouseZone
from app.repositories.base import BaseRepository


class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_inventory(self, filters=None, sorting=None, pagination=None):
        repo = BaseRepository[Inventory](self.db)
        repo.model = Inventory
        return await repo.find_all(filters, sorting, pagination)

    async def get_inventory(self, inv_id: uuid.UUID) -> Inventory:
        result = await self.db.execute(select(Inventory).where(Inventory.id == inv_id))
        inv = result.scalar_one_or_none()
        if not inv:
            raise NotFoundException("Inventory record not found")
        return inv

    async def create_transaction(
        self, inventory_id: uuid.UUID, transaction_type: TransactionType,
        quantity_change: int, reason: str, reference_type: str | None = None,
        reference_id: uuid.UUID | None = None, unit_cost: float | None = None,
        user_id: uuid.UUID | None = None
    ) -> InventoryTransaction:
        inv = await self.get_inventory(inventory_id)
        before_qty = inv.available_quantity
        after_qty = before_qty + quantity_change

        if after_qty < 0 and transaction_type not in (TransactionType.MANUAL_ADJUSTMENT,):
            raise BusinessRuleException("Insufficient inventory for this transaction")

        if transaction_type == TransactionType.GOODS_RECEIVED:
            inv.available_quantity += quantity_change
        elif transaction_type == TransactionType.SALE:
            inv.available_quantity -= abs(quantity_change)
            inv.reserved_quantity = max(0, inv.reserved_quantity - abs(quantity_change))
        elif transaction_type == TransactionType.TRANSFER_OUT:
            if inv.available_quantity < abs(quantity_change):
                raise BusinessRuleException("Insufficient stock for transfer")
            inv.available_quantity -= abs(quantity_change)
        elif transaction_type == TransactionType.TRANSFER_IN:
            inv.available_quantity += quantity_change
        elif transaction_type == TransactionType.RESERVATION:
            if inv.available_quantity < quantity_change:
                raise BusinessRuleException("Insufficient stock for reservation")
            inv.available_quantity -= quantity_change
            inv.reserved_quantity += quantity_change
        elif transaction_type == TransactionType.RELEASE:
            inv.available_quantity += abs(quantity_change)
            inv.reserved_quantity = max(0, inv.reserved_quantity - abs(quantity_change))
        else:
            inv.available_quantity = after_qty

        txn = InventoryTransaction(
            inventory_id=inventory_id, product_id=inv.product_id,
            warehouse_id=inv.warehouse_id, transaction_type=transaction_type,
            before_quantity=before_qty, after_quantity=inv.available_quantity,
            quantity_change=quantity_change,
            reference_type=reference_type, reference_id=reference_id,
            reason=reason,
            unit_cost=unit_cost, total_cost=unit_cost * abs(quantity_change) if unit_cost else None,
            created_by=user_id,
        )
        self.db.add(txn)
        await self.db.flush()
        return txn

    async def get_transaction_history(self, inventory_id: uuid.UUID):
        result = await self.db.execute(
            select(InventoryTransaction)
            .where(InventoryTransaction.inventory_id == inventory_id)
            .order_by(InventoryTransaction.created_at.desc())
            .limit(100)
        )
        return result.scalars().all()

    async def get_low_stock(self, warehouse_id: uuid.UUID | None = None):
        stmt = select(Inventory).where(
            Inventory.available_quantity <= Inventory.reorder_level,
            Inventory.reorder_level.is_not(None),
        )
        if warehouse_id:
            stmt = stmt.where(Inventory.warehouse_id == warehouse_id)
        result = await self.db.execute(stmt.limit(50))
        return result.scalars().all()

    async def get_expiring(self, days: int = 30):
        from datetime import date, timedelta
        cutoff = date.today() + timedelta(days=days)
        result = await self.db.execute(
            select(Inventory).where(
                Inventory.expiry_date <= cutoff,
                Inventory.expiry_date >= date.today(),
                Inventory.available_quantity > 0,
            ).limit(50)
        )
        return result.scalars().all()


class TransferService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transfer(self, data: dict, user_id: uuid.UUID) -> StockTransfer:
        import secrets
        from datetime import datetime
        transfer = StockTransfer(
            transfer_number=f"TRF-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}",
            from_warehouse_id=uuid.UUID(data["from_warehouse_id"]),
            to_warehouse_id=uuid.UUID(data["to_warehouse_id"]),
            status=TransferStatus.DRAFT,
            notes=data.get("notes"),
        )
        self.db.add(transfer)
        await self.db.flush()

        for item_data in data.get("items", []):
            item = StockTransferItem(
                transfer_id=transfer.id,
                product_id=uuid.UUID(item_data["product_id"]),
                inventory_id=uuid.UUID(item_data["inventory_id"]),
                quantity=item_data["quantity"],
            )
            self.db.add(item)

        await self.db.flush()
        return transfer

    async def approve_transfer(self, transfer_id: uuid.UUID, user_id: uuid.UUID):
        transfer = await self._get_transfer(transfer_id)
        if transfer.status != TransferStatus.PENDING_APPROVAL:
            raise BusinessRuleException("Transfer must be pending approval")
        transfer.status = TransferStatus.APPROVED
        transfer.approved_by = user_id
        transfer.approved_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        await self.db.flush()

    async def _get_transfer(self, transfer_id: uuid.UUID) -> StockTransfer:
        result = await self.db.execute(
            select(StockTransfer).where(StockTransfer.id == transfer_id)
        )
        transfer = result.scalar_one_or_none()
        if not transfer:
            raise NotFoundException("Transfer not found")
        return transfer


class AdjustmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_adjustment(self, data: dict, user_id: uuid.UUID) -> StockAdjustment:
        inv_result = await self.db.execute(
            select(Inventory).where(Inventory.id == uuid.UUID(data["inventory_id"]))
        )
        inv = inv_result.scalar_one_or_none()
        if not inv:
            raise NotFoundException("Inventory not found")

        before_qty = inv.available_quantity
        quantity_change = data["quantity_change"]
        after_qty = before_qty + quantity_change
        if after_qty < 0:
            raise BusinessRuleException("Adjustment would result in negative inventory")

        adj = StockAdjustment(
            inventory_id=inv.id,
            warehouse_id=inv.warehouse_id,
            adjustment_type=AdjustmentReason(data["adjustment_type"]),
            quantity_change=quantity_change,
            before_quantity=before_qty,
            after_quantity=after_qty,
            reason=data["reason"],
            created_by=user_id,
        )
        self.db.add(adj)

        inv.available_quantity = after_qty
        await self.db.flush()
        return adj


class WarehouseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_warehouses(self):
        result = await self.db.execute(select(Warehouse))
        return result.scalars().all()

    async def get_warehouse(self, wh_id: uuid.UUID) -> Warehouse:
        result = await self.db.execute(select(Warehouse).where(Warehouse.id == wh_id))
        wh = result.scalar_one_or_none()
        if not wh:
            raise NotFoundException("Warehouse not found")
        return wh

    async def create_warehouse(self, data: dict) -> Warehouse:
        repo = BaseRepository[Warehouse](self.db)
        repo.model = Warehouse
        wh = Warehouse(
            code=data["code"], name=data["name"],
            address=data.get("address"), city=data.get("city"),
            state=data.get("state"), country=data.get("country"),
            warehouse_type=data.get("warehouse_type", "Distribution"),
        )
        return await repo.create(wh)

    async def list_zones(self, warehouse_id: uuid.UUID):
        result = await self.db.execute(
            select(WarehouseZone).where(WarehouseZone.warehouse_id == warehouse_id)
        )
        return result.scalars().all()

    async def create_zone(self, warehouse_id: uuid.UUID, data: dict) -> WarehouseZone:
        repo = BaseRepository[WarehouseZone](self.db)
        repo.model = WarehouseZone
        zone = WarehouseZone(
            warehouse_id=warehouse_id, name=data["name"],
            code=data.get("code", data["name"].upper()[:10]),
            zone_type=data.get("zone_type", "Storage"),
        )
        return await repo.create(zone)
