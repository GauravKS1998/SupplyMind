from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    company_name: Mapped[str] = mapped_column(String(255))

    gst_number: Mapped[str | None] = mapped_column(String(50), nullable=True)

    contact_person: Mapped[str] = mapped_column(String(255))

    phone: Mapped[str] = mapped_column(String(20))

    address: Mapped[str] = mapped_column(String(500))

    city: Mapped[str] = mapped_column(String(100))

    state: Mapped[str] = mapped_column(String(100))

    country: Mapped[str] = mapped_column(String(100))

    pincode: Mapped[str] = mapped_column(String(20))

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    verified_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

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

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user = relationship("User")
