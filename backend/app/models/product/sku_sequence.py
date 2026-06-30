"""SKU Sequence model for auto-incrementing per category-brand combinations."""
import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseEntity


class SKUSequence(BaseEntity):
    __tablename__ = "sku_sequences"

    category_prefix: Mapped[str] = mapped_column(String(10), nullable=False)
    brand_code: Mapped[str] = mapped_column(String(10), nullable=False)
    current_sequence: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
