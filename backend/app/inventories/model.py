from sqlalchemy import (
    Date,
    Integer,
    Boolean,
    ForeignKey,
    String,
    DateTime,
    Float,
    Numeric,
)

from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date, datetime, timezone

from app.database.database import Base


class Inventory(Base):

    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)

    available_quantity: Mapped[int] = mapped_column(Integer)

    unit_cost: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    reorder_level: Mapped[int] = mapped_column(Integer)

    reorder_quantity: Mapped[int] = mapped_column(Integer)

    batch_number: Mapped[str] = mapped_column(String(100))

    manufacturing_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    storage_location: Mapped[str | None] = mapped_column(String(100), nullable=True)

    last_movement_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    deactivated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    reactivated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    product = relationship("Product")
    warehouse = relationship("Warehouse")
