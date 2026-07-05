from sqlalchemy import Integer, String, Boolean, Float, DateTime, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base


class Warehouse(Base):

    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    warehouse_code: Mapped[str] = mapped_column(String(100), unique=True)

    name: Mapped[str] = mapped_column(String(255))

    warehouse_type: Mapped[str] = mapped_column(String(100))

    manager_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    capacity: Mapped[float] = mapped_column(Float)

    current_utilization: Mapped[float] = mapped_column(Float, default=0.0)

    address: Mapped[str] = mapped_column(String(500))

    city: Mapped[str] = mapped_column(String(100))

    state: Mapped[str] = mapped_column(String(100))

    country: Mapped[str] = mapped_column(String(100))

    postal_code: Mapped[str] = mapped_column(String(20))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

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

    manager = relationship("User")
