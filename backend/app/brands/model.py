from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
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
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
