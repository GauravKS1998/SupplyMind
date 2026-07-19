from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

from sqlalchemy import Enum

from .enums import InventoryTransactionType, InventoryReferenceType


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)

    inventory_id = Column(
        Integer,
        ForeignKey("inventories.id"),
        nullable=False,
    )

    transaction_type = Column(
        Enum(InventoryTransactionType),
        nullable=False,
    )

    quantity_before = Column(
        Integer,
        nullable=False,
    )

    quantity_delta = Column(
        Integer,
        nullable=False,
    )

    quantity_after = Column(
        Integer,
        nullable=False,
    )

    reserved_quantity_before = Column(
        Integer,
        nullable=False,
    )

    reserved_quantity_after = Column(
        Integer,
        nullable=False,
    )

    available_quantity_before = Column(
        Integer,
        nullable=False,
    )

    available_quantity_after = Column(
        Integer,
        nullable=False,
    )

    reason = Column(
        String,
        nullable=True,
    )

    reference_type = Column(
        Enum(InventoryReferenceType),
        nullable=True,
    )

    reference_id = Column(
        Integer,
        nullable=True,
    )

    created_by = Column(
        Integer,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    inventory = relationship(
        "Inventory",
        back_populates="transactions",
    )

    transactions = relationship(
        "InventoryTransaction",
        back_populates="inventory",
    )
