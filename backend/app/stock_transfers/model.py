from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database.database import Base
from .enums import TransferStatus


class StockTransfer(Base):

    __tablename__ = "stock_transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    source_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    destination_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))

    quantity: Mapped[int] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String(50), default=TransferStatus.INITIATED)

    initiated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    rejected_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    cancelled_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    completed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    transferred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    product = relationship("Product")

    source_warehouse = relationship("Warehouse", foreign_keys=[source_warehouse_id])

    destination_warehouse = relationship(
        "Warehouse", foreign_keys=[destination_warehouse_id]
    )
