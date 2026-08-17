from __future__ import annotations

from datetime import datetime, timezone

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

from .enums import TransferStatus


class StockTransfer(Base):

    __tablename__ = "stock_transfers"

    __table_args__ = (
        UniqueConstraint(
            "transfer_number",
            name="uq_stock_transfer_number",
        ),
        Index(
            "idx_stock_transfer_number",
            "transfer_number",
        ),
        Index(
            "idx_stock_transfer_source_warehouse",
            "source_warehouse_id",
        ),
        Index(
            "idx_stock_transfer_destination_warehouse",
            "destination_warehouse_id",
        ),
        Index(
            "idx_stock_transfer_status",
            "status",
        ),
        Index(
            "idx_stock_transfer_created_at",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    transfer_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    destination_warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    status: Mapped[TransferStatus] = mapped_column(
        String(30),
        nullable=False,
        default=TransferStatus.INITIATED,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    initiated_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    rejected_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    cancelled_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    completed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    source_warehouse = relationship(
        "Warehouse",
        foreign_keys=[source_warehouse_id],
    )

    destination_warehouse = relationship(
        "Warehouse",
        foreign_keys=[destination_warehouse_id],
    )

    lines = relationship(
        "StockTransferLine",
        back_populates="stock_transfer",
        cascade="all, delete-orphan",
    )


class StockTransferLine(Base):

    __tablename__ = "stock_transfer_lines"

    __table_args__ = (
        UniqueConstraint(
            "stock_transfer_id",
            "line_number",
            name="uq_stock_transfer_line_number",
        ),
        Index(
            "idx_stock_transfer_line_transfer",
            "stock_transfer_id",
        ),
        Index(
            "idx_stock_transfer_line_product",
            "product_id",
        ),
        Index(
            "idx_stock_transfer_line_source_inventory",
            "source_inventory_id",
        ),
        Index(
            "idx_stock_transfer_line_destination_inventory",
            "destination_inventory_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    stock_transfer_id: Mapped[int] = mapped_column(
        ForeignKey("stock_transfers.id"),
        nullable=False,
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    source_inventory_id: Mapped[int] = mapped_column(
        ForeignKey("inventories.id"),
        nullable=False,
    )

    destination_inventory_id: Mapped[int | None] = mapped_column(
        ForeignKey("inventories.id"),
        nullable=True,
    )

    batch_number: Mapped[str] = mapped_column(
        String(100),
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

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    stock_transfer: Mapped["StockTransfer"] = relationship(
        back_populates="lines",
    )

    product = relationship("Product")

    source_inventory = relationship(
        "Inventory",
        foreign_keys=[source_inventory_id],
    )

    destination_inventory = relationship(
        "Inventory",
        foreign_keys=[destination_inventory_id],
    )
