from sqlalchemy import Integer, ForeignKey, DateTime

from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, timezone

from app.database.database import Base


class StockTransfer(Base):

    __tablename__ = "stock_transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    source_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    destination_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    transferred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
