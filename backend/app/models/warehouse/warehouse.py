import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseEntity, SoftDeleteMixin


class Warehouse(BaseEntity, SoftDeleteMixin, AuditMixin):
    __tablename__ = "warehouses"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata", nullable=False)
    working_hours_start: Mapped[str | None] = mapped_column(String(5), nullable=True)
    working_hours_end: Mapped[str | None] = mapped_column(String(5), nullable=True)
    manager_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    warehouse_type: Mapped[str] = mapped_column(String(50), default="Distribution", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    zones: Mapped[list["WarehouseZone"]] = relationship("WarehouseZone", back_populates="warehouse")


class WarehouseZone(BaseEntity, SoftDeleteMixin, AuditMixin):
    __tablename__ = "warehouse_zones"

    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    zone_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="zones")
    bins: Mapped[list["WarehouseBin"]] = relationship("WarehouseBin", back_populates="zone")


class WarehouseBin(BaseEntity, SoftDeleteMixin, AuditMixin):
    __tablename__ = "warehouse_bins"

    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouse_zones.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    rack: Mapped[str | None] = mapped_column(String(50), nullable=True)
    shelf: Mapped[str | None] = mapped_column(String(50), nullable=True)
    max_capacity: Mapped[int | None] = mapped_column(nullable=True)
    current_capacity: Mapped[int | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    zone: Mapped["WarehouseZone"] = relationship("WarehouseZone", back_populates="bins")
