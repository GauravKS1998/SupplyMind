from sqlalchemy import Integer, Float, ForeignKey, DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base


class SalesOrder(Base):

    __tablename__ = "sales_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    total_price: Mapped[float] = mapped_column(Float)

    sold_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    product = relationship("Product")
    warehouse = relationship("Warehouse")
