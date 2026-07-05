from sqlalchemy import Integer, Boolean, ForeignKey, String, Date, DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base


class Inventory(Base):

    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)

    available_quantity: Mapped[int] = mapped_column(Integer)

    reorder_level: Mapped[int] = mapped_column(Integer)

    reorder_quantity: Mapped[int] = mapped_column(Integer)

    batch_number: Mapped[str] = mapped_column(String(100))

    expiry_date: Mapped[Date] = mapped_column(nullable=True)

    last_stocked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    product = relationship("Product")
    warehouse = relationship("Warehouse")
