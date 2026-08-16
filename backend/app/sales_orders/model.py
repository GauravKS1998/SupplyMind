from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
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
from .enums import SalesOrderStatus


class SalesOrder(Base):

    __tablename__ = "sales_orders"

    __table_args__ = (
        UniqueConstraint(
            "so_number",
            name="uq_sales_order_so_number",
        ),
        Index(
            "idx_sales_order_status",
            "status",
        ),
        Index(
            "idx_sales_order_customer",
            "customer_id",
        ),
        Index(
            "idx_sales_order_warehouse",
            "warehouse_id",
        ),
        Index(
            "idx_sales_order_created_at",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    so_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    status: Mapped[SalesOrderStatus] = mapped_column(
        String(30),
        default=SalesOrderStatus.DRAFT,
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    discount_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    tax_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    confirmed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    dispatched_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    delivered_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    completed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    cancelled_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    returned_by: Mapped[int | None] = mapped_column(
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

    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    returned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    customer = relationship(
        "User",
    )

    warehouse = relationship(
        "Warehouse",
    )

    lines: Mapped[list["SalesOrderLine"]] = relationship(
        back_populates="sales_order",
        cascade="all, delete-orphan",
    )


class SalesOrderLine(Base):

    __tablename__ = "sales_order_lines"

    __table_args__ = (
        UniqueConstraint(
            "sales_order_id",
            "line_number",
            name="uq_sales_order_line_number",
        ),
        Index(
            "idx_sales_order_line_sales_order",
            "sales_order_id",
        ),
        Index(
            "idx_sales_order_line_product",
            "product_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    sales_order_id: Mapped[int] = mapped_column(
        ForeignKey("sales_orders.id"),
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

    product_name_snapshot: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    product_sku_snapshot: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    inventory_id: Mapped[int | None] = mapped_column(
        ForeignKey("inventories.id"),
        nullable=True,
    )

    ordered_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sales_order = relationship(
        "SalesOrder",
        back_populates="lines",
    )

    product = relationship(
        "Product",
    )

    inventory = relationship(
        "Inventory",
    )
