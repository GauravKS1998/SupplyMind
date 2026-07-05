from sqlalchemy import Integer, String, ForeignKey, DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base

from .enums import PurchaseOrderStatus


class PurchaseOrder(Base):

    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    po_number: Mapped[str] = mapped_column(String(100), unique=True)

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String(50), default=PurchaseOrderStatus.DRAFT)

    expected_delivery_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    actual_delivery_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    supplier = relationship("Supplier")
    product = relationship("Product")
    warehouse = relationship("Warehouse")
