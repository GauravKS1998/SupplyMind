from sqlalchemy import (
    Integer,
    String,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from datetime import datetime, timezone

from app.database.database import Base

class Warehouse(Base):

    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[String] = mapped_column(
        String(255)
    )

    location: Mapped[String] = mapped_column(
        String(255)
    )

    capacity: Mapped[int] = mapped_column(
        Integer
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc) # Similar to @CreationTimestamp
    )