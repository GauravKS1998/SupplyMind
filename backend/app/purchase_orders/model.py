from sqlalchemy import Integer, String, DateTime, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base


class PurchaseOrder(Base):

    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String(50), default="PENDING")

    ordered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    supplier = relationship("Supplier")
    product = relationship("Product")
    warehouse = relationship("Warehouse")
