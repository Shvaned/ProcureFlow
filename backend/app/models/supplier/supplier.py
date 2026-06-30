import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseEntity, SoftDeleteMixin


class Supplier(BaseEntity, SoftDeleteMixin, AuditMixin):
    __tablename__ = "suppliers"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    legal_name: Mapped[str] = mapped_column(String(500), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gst_number: Mapped[str | None] = mapped_column(String(15), unique=True, nullable=True)
    pan: Mapped[str | None] = mapped_column(String(10), unique=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    payment_terms: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_preferred: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    contacts: Mapped[list["SupplierContact"]] = relationship("SupplierContact", back_populates="supplier")
    addresses: Mapped[list["SupplierAddress"]] = relationship("SupplierAddress", back_populates="supplier")
    documents: Mapped[list["SupplierDocument"]] = relationship("SupplierDocument", back_populates="supplier")
    performance: Mapped["SupplierPerformance | None"] = relationship(
        "SupplierPerformance", back_populates="supplier", uselist=False
    )


class SupplierContact(BaseEntity):
    __tablename__ = "supplier_contacts"

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    designation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contact_type: Mapped[str] = mapped_column(String(50), default="General", nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="contacts")


class SupplierAddress(BaseEntity):
    __tablename__ = "supplier_addresses"

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False
    )
    address_type: Mapped[str] = mapped_column(String(50), nullable=False)
    line1: Mapped[str] = mapped_column(String(500), nullable=False)
    line2: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="addresses")


class SupplierDocument(BaseEntity):
    __tablename__ = "supplier_documents"

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expiry_date: Mapped[str | None] = mapped_column(String(50), nullable=True)

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="documents")


class SupplierPerformance(BaseEntity):
    __tablename__ = "supplier_performance"

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    avg_lead_time_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    late_deliveries_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rejected_goods_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    quality_rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    delivery_rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    price_competitiveness: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_purchase_orders: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    on_time_delivery_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="performance")
