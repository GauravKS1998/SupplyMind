from sqlalchemy import Integer, String, Boolean, Float, DateTime, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.database import Base


class Supplier(Base):

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    company_name: Mapped[str] = mapped_column(String(255))

    gst_number: Mapped[str] = mapped_column(String(100), unique=True)

    contact_person: Mapped[str] = mapped_column(String(255))

    phone: Mapped[str] = mapped_column(String(20))

    email: Mapped[str] = mapped_column(String(255))

    address: Mapped[str] = mapped_column(String(500))

    city: Mapped[str] = mapped_column(String(100))

    state: Mapped[str] = mapped_column(String(100))

    country: Mapped[str] = mapped_column(String(100))

    postal_code: Mapped[str] = mapped_column(String(20))

    supplier_type: Mapped[str] = mapped_column(String(100))

    lead_time_days: Mapped[int] = mapped_column(Integer)

    payment_terms: Mapped[str] = mapped_column(String(100))

    rating: Mapped[float] = mapped_column(Float, default=0.0)

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User")
