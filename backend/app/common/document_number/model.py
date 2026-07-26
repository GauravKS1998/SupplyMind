from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

from .enums import DocumentType


class DocumentSequence(Base):
    __tablename__ = "document_sequences"

    __table_args__ = (
        UniqueConstraint(
            "document_type",
            "sequence_date",
            name="uq_document_sequence_type_date",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    document_type: Mapped[DocumentType] = mapped_column(
        Enum(DocumentType),
        nullable=False,
    )

    sequence_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    last_sequence: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
