from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, timezone

from app.database.database import Base

from .enums import UserRole, ApprovalStatus


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[str] = mapped_column(String(100), unique=True)

    email: Mapped[str] = mapped_column(String(255), unique=True)

    password_hash: Mapped[str] = mapped_column(String(255))

    role: Mapped[UserRole] = mapped_column(String(50))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    approval_status: Mapped[ApprovalStatus] = mapped_column(
        String(50), default=ApprovalStatus.APPROVED
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
