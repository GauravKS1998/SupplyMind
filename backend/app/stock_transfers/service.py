from sqlalchemy.orm import Session

from datetime import datetime, timezone

from .model import StockTransfer

from .schema import StockTransferRequest, StockTransferResponse

from app.inventories.repository import find_by_product_and_warehouse

from .repository import save_transfer, find_transfer_by_id

from .enums import TransferStatus

from .exceptions import (
    SourceInventoryNotFoundException,
    DestinationInventoryNotFoundException,
    InsufficientStockException,
    InvalidTransferRequestException,
    TransferFailedException,
    TransferNotFoundException,
    TransferNotInitiatedException,
    TransferNotApprovedException,
    TransferNotInTransitException,
)

from app.logging.logger import logger


def initiate_transfer(db: Session, request: StockTransferRequest, current_user_id: int):
    if request.source_warehouse_id == request.destination_warehouse_id:
        raise InvalidTransferRequestException("Source and destination cannot be same")

    source_inventory = find_by_product_and_warehouse(
        db, request.product_id, request.source_warehouse_id
    )

    destination_inventory = find_by_product_and_warehouse(
        db, request.product_id, request.destination_warehouse_id
    )

    if not source_inventory:
        raise SourceInventoryNotFoundException("Source inventory not found")

    if not destination_inventory:
        raise DestinationInventoryNotFoundException("Destination inventory not found")

    if source_inventory.available_quantity < request.quantity:
        raise InsufficientStockException("Insufficient available stock")

    try:
        source_inventory.reserved_quantity += request.quantity
        source_inventory.available_quantity -= request.quantity

        transfer = StockTransfer(
            product_id=request.product_id,
            source_warehouse_id=request.source_warehouse_id,
            destination_warehouse_id=request.destination_warehouse_id,
            quantity=request.quantity,
            status=TransferStatus.INITIATED,
            initiated_by=current_user_id,
        )

        saved_transfer = save_transfer(db, transfer)

        db.commit()
        db.refresh(saved_transfer)

        logger.info(f"Stock transfer {saved_transfer.id} initiated")

        return StockTransferResponse(
            id=saved_transfer.id,
            product_id=saved_transfer.product_id,
            product_name=saved_transfer.product.name,
            product_sku=saved_transfer.product.sku,
            source_warehouse_id=saved_transfer.source_warehouse_id,
            source_warehouse_name=saved_transfer.source_warehouse.name,
            destination_warehouse_id=saved_transfer.destination_warehouse_id,
            destination_warehouse_name=saved_transfer.destination_warehouse.name,
            quantity=saved_transfer.quantity,
            status=saved_transfer.status,
            transferred_at=saved_transfer.transferred_at,
            completed_at=saved_transfer.completed_at,
        )

    except Exception:
        db.rollback()  # Equivalent to @Transactional: if succeeds save otherwise rollback

        raise TransferFailedException("Transfer failed and rolled back")


def approve_transfer(db: Session, transfer_id: int, current_user_id: int):
    transfer = find_transfer_by_id(db, transfer_id)

    if not transfer:
        raise TransferNotFoundException("Transfer not found")

    if transfer.status != TransferStatus.INITIATED:
        raise TransferNotInitiatedException("Only initiated transfers can be approved")

    try:
        transfer.status = TransferStatus.APPROVED
        transfer.approved_by = current_user_id
        transfer.updated_by = current_user_id
        transfer.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(transfer)

        logger.info(f"Stock transfer {transfer.id} approved")

        return {"message": "Transfer approved successfully"}

    except Exception:
        db.rollback()
        raise TransferFailedException("Transfer approval failed and rolled back")


def reject_transfer(db: Session, transfer_id: int, current_user_id: int):
    transfer = find_transfer_by_id(db, transfer_id)

    if not transfer:
        raise TransferNotFoundException("Transfer not found")

    if transfer.status != TransferStatus.INITIATED:
        raise TransferNotInitiatedException("Only initiated transfers can be rejected")

    source_inventory = find_by_product_and_warehouse(
        db, transfer.product_id, transfer.source_warehouse_id
    )

    try:
        source_inventory.reserved_quantity -= transfer.quantity
        source_inventory.available_quantity += transfer.quantity

        transfer.status = TransferStatus.REJECTED
        transfer.rejected_by = current_user_id
        transfer.updated_by = current_user_id
        transfer.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(transfer)

        logger.info(f"Stock transfer {transfer.id} rejected")

        return {"message": "Transfer rejected successfully"}

    except Exception:
        db.rollback()
        raise TransferFailedException("Transfer rejection failed and rolled back")


def mark_in_transit(db: Session, transfer_id: int, current_user_id: int):
    transfer = find_transfer_by_id(db, transfer_id)

    if not transfer:
        raise TransferNotFoundException("Transfer not found")

    if transfer.status != TransferStatus.APPROVED:
        raise TransferNotApprovedException(
            "Only approved transfers can move to transit"
        )

    try:
        transfer.status = TransferStatus.IN_TRANSIT
        transfer.updated_by = current_user_id
        transfer.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(transfer)

        logger.info(f"Stock transfer {transfer.id} in transit")

        return {"message": "Transfer is now in transit"}

    except Exception:
        db.rollback()
        raise TransferFailedException(
            "Marking transfer in transit failed and rolled back"
        )


def complete_transfer(db: Session, transfer_id: int, current_user_id: int):
    transfer = find_transfer_by_id(db, transfer_id)

    if not transfer:
        raise TransferNotFoundException("Transfer not found")

    if transfer.status != TransferStatus.IN_TRANSIT:
        raise TransferNotInTransitException("Only in-transit transfers can complete")

    source_inventory = find_by_product_and_warehouse(
        db, transfer.product_id, transfer.source_warehouse_id
    )

    destination_inventory = find_by_product_and_warehouse(
        db, transfer.product_id, transfer.destination_warehouse_id
    )

    try:
        source_inventory.quantity -= transfer.quantity
        source_inventory.reserved_quantity -= transfer.quantity

        destination_inventory.quantity += transfer.quantity
        destination_inventory.available_quantity += transfer.quantity

        transfer.status = TransferStatus.COMPLETED
        transfer.completed_at = datetime.now(timezone.utc)
        transfer.completed_by = current_user_id
        transfer.updated_by = current_user_id
        transfer.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(transfer)

        logger.info(f"Stock transfer {transfer.id} completed")

        return {"message": "Transfer completed successfully"}

    except Exception:
        db.rollback()
        raise TransferFailedException("Completing transfer failed and rolled back")


def cancel_transfer(db: Session, transfer_id: int, current_user_id: int):
    transfer = find_transfer_by_id(db, transfer_id)

    if not transfer:
        raise TransferNotFoundException("Transfer not found")

    if transfer.status not in {TransferStatus.INITIATED, TransferStatus.APPROVED}:
        raise TransferNotInitiatedException(
            "Only initiated or approved transfers can be cancelled"
        )

    source_inventory = find_by_product_and_warehouse(
        db, transfer.product_id, transfer.source_warehouse_id
    )

    try:
        source_inventory.reserved_quantity -= transfer.quantity
        source_inventory.available_quantity += transfer.quantity

        transfer.status = TransferStatus.CANCELLED
        transfer.cancelled_by = current_user_id
        transfer.updated_by = current_user_id
        transfer.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(transfer)

        logger.info(f"Stock transfer {transfer.id} cancelled")

        return {"message": "Transfer cancelled successfully"}

    except Exception:
        db.rollback()
        raise TransferFailedException("Cancelling transfer failed and rolled back")
