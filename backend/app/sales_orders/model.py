from sqlalchemy import Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database.database import Base
from .enums import SalesOrderStatus


class SalesOrder(Base):

    __tablename__ = "sales_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    so_number: Mapped[str] = mapped_column(String(100), unique=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    total_price: Mapped[float] = mapped_column(Float)

    status: Mapped[str] = mapped_column(String(50), default=SalesOrderStatus.DRAFT)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    confirmed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    dispatched_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    delivered_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    completed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    cancelled_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    returned_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    sold_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    returned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    product = relationship("Product")
    warehouse = relationship("Warehouse")
