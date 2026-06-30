import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import JSON, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseEntity


class DailyMetrics(BaseEntity):
    __tablename__ = "daily_metrics"

    metric_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    warehouse_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True
    )
    total_revenue: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    total_orders: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_inventory_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    total_procurement_spend: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    low_stock_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    out_of_stock_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pending_approvals: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    metrics_json: Mapped[str | None] = mapped_column(JSON, nullable=True)


class KPISnapshot(BaseEntity):
    __tablename__ = "kpi_snapshots"

    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    kpi_key: Mapped[str] = mapped_column(String(100), nullable=False)
    kpi_value: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    kpi_target: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    trend_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    warehouse_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True
    )
    metadata_json: Mapped[str | None] = mapped_column(JSON, nullable=True)
