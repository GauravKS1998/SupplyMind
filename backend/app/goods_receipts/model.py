from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base
from app.goods_receipts.enums import GoodsReceiptStatus
from app.products.model import Product
from app.warehouses.model import Warehouse

if TYPE_CHECKING:
    from app.purchase_orders.model import PurchaseOrder, PurchaseOrderLine


class GoodsReceipt(Base):
    __tablename__ = "goods_receipts"

    __table_args__ = (
        UniqueConstraint(
            "grn_number",
            name="uq_goods_receipt_grn_number",
        ),
        Index("idx_goods_receipt_grn_number", "grn_number"),
        Index("idx_goods_receipt_purchase_order", "purchase_order_id"),
        Index("idx_goods_receipt_warehouse", "warehouse_id"),
        Index("idx_goods_receipt_status", "status"),
        Index("idx_goods_receipt_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    grn_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    purchase_order_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=False,
    )

    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    status: Mapped[GoodsReceiptStatus] = mapped_column(
        nullable=False,
        default=GoodsReceiptStatus.DRAFT,
    )

    remarks: Mapped[str | None] = mapped_column(Text)

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    received_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    cancelled_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        "PurchaseOrder",
        back_populates="goods_receipts",
    )

    warehouse: Mapped["Warehouse"] = relationship()

    lines: Mapped[list["GoodsReceiptLine"]] = relationship(
        back_populates="goods_receipt",
        cascade="all, delete-orphan",
    )


class GoodsReceiptLine(Base):
    __tablename__ = "goods_receipt_lines"

    __table_args__ = (
        UniqueConstraint(
            "goods_receipt_id",
            "line_number",
            name="uq_goods_receipt_line_number",
        ),
        Index(
            "idx_goods_receipt_line_goods_receipt",
            "goods_receipt_id",
        ),
        Index(
            "idx_goods_receipt_line_product",
            "product_id",
        ),
        Index(
            "idx_goods_receipt_line_purchase_order_line",
            "purchase_order_line_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    goods_receipt_id: Mapped[int] = mapped_column(
        ForeignKey("goods_receipts.id"),
        nullable=False,
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    purchase_order_line_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_order_lines.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    product_name_snapshot: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    product_sku_snapshot: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    batch_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    accepted_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    rejected_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    remarks: Mapped[str | None] = mapped_column(Text)

    goods_receipt: Mapped["GoodsReceipt"] = relationship(
        "GoodsReceipt",
        back_populates="lines",
    )

    purchase_order_line: Mapped["PurchaseOrderLine"] = relationship(
        "PurchaseOrderLine",
    )

    product: Mapped["Product"] = relationship()
