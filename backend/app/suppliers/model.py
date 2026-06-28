from sqlalchemy import Integer, String, DateTime

from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, timezone

from app.database.database import Base


class Supplier(Base):

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255))

    contact_email: Mapped[str] = mapped_column(
        String(255), unique=True
    )  # Similar to @Column(unique = true)

    phone: Mapped[str] = mapped_column(String(20))

    address: Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
