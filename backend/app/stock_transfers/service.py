from __future__ import annotations

from datetime import datetime, timezone
from math import ceil

from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise
from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse

from app.common.document_number.enums import DocumentType
from app.common.document_number.service import get_next_document_number

from app.inventories.model import Inventory

from app.inventory_transactions.enums import InventoryReferenceType
from app.inventories.repository import (
    find_by_id as find_inventory_by_id,
    find_duplicate_inventory,
)
from app.inventories.service import (
    create_inventory_transaction,
    reserve_inventory_transaction,
    release_inventory_transaction,
    increase_inventory_transaction,
    decrease_inventory_transaction,
)

from app.logging.logger import logger

from .enums import TransferStatus

from .exceptions import (
    StockTransferNotFoundException,
    InvalidStockTransferException,
)

from .mapper import (
    map_stock_transfer,
    map_stock_transfers,
)

from .model import (
    StockTransfer,
    StockTransferLine,
)

from .repository import (
    find_stock_transfer_by_id,
    save_stock_transfer,
    search_stock_transfers as find_stock_transfers,
)

from .schema import (
    StockTransferCreateRequest,
    StockTransferLineCreateRequest,
    StockTransferLineUpdateRequest,
    StockTransferResponse,
    StockTransferSearchRequest,
    StockTransferUpdateRequest,
)

from .validators import (
    validate_approve_stock_transfer,
    validate_batch_number,
    validate_cancel_stock_transfer,
    validate_complete_stock_transfer,
    validate_different_warehouses,
    validate_duplicate_transfer_lines,
    validate_initiated_stock_transfer,
    validate_product_exists,
    validate_source_inventory,
    validate_stock_transfer_line_exists,
    validate_stock_transfer_lines,
    validate_transfer_quantity,
    validate_warehouse_exists,
    validate_transit_stock_transfer,
    validate_reject_stock_transfer,
)


def _build_stock_transfer_lines(
    db: Session,
    request_lines: list[StockTransferLineCreateRequest],
) -> list[StockTransferLine]:

    stock_transfer_lines = []

    for request_line in request_lines:

        stock_transfer_lines.append(
            _create_stock_transfer_line(
                db,
                request_line,
            )
        )

    _renumber_stock_transfer_lines(
        stock_transfer_lines,
    )

    return stock_transfer_lines


def _create_stock_transfer_line(
    db: Session,
    request_line: StockTransferLineCreateRequest | StockTransferLineUpdateRequest,
) -> StockTransferLine:

    product = validate_product_exists(
        db,
        request_line.product_id,
    )

    validate_transfer_quantity(
        request_line.quantity,
    )

    validate_batch_number(
        request_line.batch_number,
    )

    return StockTransferLine(
        product_id=product.id,
        product_name_snapshot=product.name,
        product_sku_snapshot=product.sku,
        batch_number=request_line.batch_number.strip(),
        quantity=request_line.quantity,
        remarks=request_line.remarks,
    )


def _update_stock_transfer_line(
    db: Session,
    stock_transfer_line: StockTransferLine,
    request_line: StockTransferLineUpdateRequest,
):

    product = validate_product_exists(
        db,
        request_line.product_id,
    )

    validate_transfer_quantity(
        request_line.quantity,
    )

    validate_batch_number(
        request_line.batch_number,
    )

    stock_transfer_line.product_id = product.id

    stock_transfer_line.product_name_snapshot = product.name

    stock_transfer_line.product_sku_snapshot = product.sku

    stock_transfer_line.batch_number = request_line.batch_number.strip()

    stock_transfer_line.quantity = request_line.quantity

    stock_transfer_line.remarks = request_line.remarks


def _find_stock_transfer_line(
    stock_transfer: StockTransfer,
    stock_transfer_line_id: int,
) -> StockTransferLine | None:

    return next(
        (line for line in stock_transfer.lines if line.id == stock_transfer_line_id),
        None,
    )


def _delete_stock_transfer_lines(
    stock_transfer: StockTransfer,
    deleted_line_ids: list[int],
):

    for deleted_line_id in deleted_line_ids:

        stock_transfer_line = validate_stock_transfer_line_exists(
            stock_transfer,
            deleted_line_id,
        )

        stock_transfer.lines.remove(
            stock_transfer_line,
        )


def _renumber_stock_transfer_lines(
    stock_transfer_lines: list[StockTransferLine],
):

    for index, line in enumerate(
        stock_transfer_lines,
        start=1,
    ):
        line.line_number = index


def _populate_stock_transfer_header(
    stock_transfer: StockTransfer,
    request: StockTransferCreateRequest | StockTransferUpdateRequest,
):

    stock_transfer.source_warehouse_id = request.source_warehouse_id

    stock_transfer.destination_warehouse_id = request.destination_warehouse_id

    stock_transfer.remarks = request.remarks


def _get_stock_transfer(
    db: Session,
    stock_transfer_id: int,
) -> StockTransfer:

    return get_or_raise(
        find_stock_transfer_by_id(
            db,
            stock_transfer_id,
        ),
        StockTransferNotFoundException(
            f"Stock Transfer with id '{stock_transfer_id}' was not found."
        ),
    )


def _get_or_create_destination_inventory(
    db: Session,
    line: StockTransferLine,
    source_inventory: Inventory,
    destination_warehouse_id: int,
    current_user_id: int,
    stock_transfer: StockTransfer,
) -> Inventory:

    destination_inventory = find_duplicate_inventory(
        db=db,
        product_id=line.product_id,
        warehouse_id=destination_warehouse_id,
        batch_number=line.batch_number,
    )

    if destination_inventory:

        if not destination_inventory.is_active:
            raise InvalidStockTransferException(
                f"Destination inventory '{destination_inventory.id}' "
                f"for product '{line.product_id}' and batch "
                f"'{line.batch_number}' is inactive."
            )

        return destination_inventory

    return create_inventory_transaction(
        db=db,
        product_id=line.product_id,
        warehouse_id=destination_warehouse_id,
        quantity=0,
        unit_cost=source_inventory.unit_cost,
        reorder_level=source_inventory.reorder_level,
        reorder_quantity=source_inventory.reorder_quantity,
        batch_number=line.batch_number,
        manufacturing_date=source_inventory.manufacturing_date,
        expiry_date=source_inventory.expiry_date,
        storage_location=None,
        current_user_id=current_user_id,
        reason=(
            f"Destination inventory created for "
            f"Stock Transfer '{stock_transfer.transfer_number}'."
        ),
        reference_type=InventoryReferenceType.STOCK_TRANSFER,
        reference_id=stock_transfer.id,
    )


def create_stock_transfer(
    db: Session,
    request: StockTransferCreateRequest,
    initiated_by: int,
) -> StockTransferResponse:

    logger.info(
        "Creating Stock Transfer from warehouse_id=%s " "to warehouse_id=%s",
        request.source_warehouse_id,
        request.destination_warehouse_id,
    )

    validate_different_warehouses(
        request.source_warehouse_id,
        request.destination_warehouse_id,
    )

    validate_warehouse_exists(
        db,
        request.source_warehouse_id,
    )

    validate_warehouse_exists(
        db,
        request.destination_warehouse_id,
    )

    validate_stock_transfer_lines(
        request.lines,
    )

    validate_duplicate_transfer_lines(
        request.lines,
    )

    transfer_number = get_next_document_number(
        db=db,
        document_type=DocumentType.STOCK_TRANSFER,
    )

    stock_transfer = StockTransfer(
        transfer_number=transfer_number,
        status=TransferStatus.INITIATED,
        initiated_by=initiated_by,
    )

    _populate_stock_transfer_header(
        stock_transfer,
        request,
    )

    stock_transfer.lines = _build_stock_transfer_lines(
        db,
        request.lines,
    )

    save_stock_transfer(
        db,
        stock_transfer,
    )

    db.commit()
    db.refresh(
        stock_transfer,
    )

    logger.info(
        "Stock Transfer %s created successfully.",
        stock_transfer.transfer_number,
    )

    return map_stock_transfer(
        stock_transfer,
    )


def update_stock_transfer(
    db: Session,
    stock_transfer_id: int,
    request: StockTransferUpdateRequest,
    updated_by: int,
) -> StockTransferResponse:

    logger.info(
        "Updating Stock Transfer id=%s",
        stock_transfer_id,
    )

    stock_transfer = _get_stock_transfer(
        db,
        stock_transfer_id,
    )

    validate_initiated_stock_transfer(
        stock_transfer,
    )

    validate_different_warehouses(
        request.source_warehouse_id,
        request.destination_warehouse_id,
    )

    validate_warehouse_exists(
        db,
        request.source_warehouse_id,
    )

    validate_warehouse_exists(
        db,
        request.destination_warehouse_id,
    )

    validate_stock_transfer_lines(
        request.lines,
    )

    validate_duplicate_transfer_lines(
        request.lines,
    )

    _populate_stock_transfer_header(
        stock_transfer,
        request,
    )

    for request_line in request.lines:

        if request_line.id is None:

            stock_transfer.lines.append(
                _create_stock_transfer_line(
                    db,
                    request_line,
                )
            )

            continue

        stock_transfer_line = validate_stock_transfer_line_exists(
            stock_transfer,
            request_line.id,
        )

        _update_stock_transfer_line(
            db,
            stock_transfer_line,
            request_line,
        )

    _delete_stock_transfer_lines(
        stock_transfer,
        request.deleted_line_ids,
    )

    _renumber_stock_transfer_lines(
        stock_transfer.lines,
    )

    stock_transfer.updated_by = updated_by

    db.commit()
    db.refresh(
        stock_transfer,
    )

    logger.info(
        "Stock Transfer %s updated successfully.",
        stock_transfer.transfer_number,
    )

    return map_stock_transfer(
        stock_transfer,
    )


def get_stock_transfer(
    db: Session,
    stock_transfer_id: int,
) -> StockTransferResponse:

    stock_transfer = _get_stock_transfer(
        db,
        stock_transfer_id,
    )

    return map_stock_transfer(
        stock_transfer,
    )


def search_stock_transfers(
    db: Session,
    request: StockTransferSearchRequest,
):

    logger.info("Searching stock transfers.")

    stock_transfers, total_items = find_stock_transfers(
        db,
        request,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_stock_transfers(
            stock_transfers,
        ),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


def approve_stock_transfer(
    db: Session,
    stock_transfer_id: int,
    approved_by: int,
) -> StockTransferResponse:

    logger.info(
        "Approving Stock Transfer id=%s",
        stock_transfer_id,
    )

    stock_transfer = _get_stock_transfer(
        db,
        stock_transfer_id,
    )

    validate_approve_stock_transfer(
        stock_transfer,
    )

    for line in stock_transfer.lines:

        inventory = validate_source_inventory(
            db=db,
            product_id=line.product_id,
            warehouse_id=stock_transfer.source_warehouse_id,
            batch_number=line.batch_number,
            quantity=line.quantity,
        )

        reserve_inventory_transaction(
            db=db,
            inventory=inventory,
            quantity=line.quantity,
            current_user_id=approved_by,
            reason=(
                f"Stock Transfer " f"{stock_transfer.transfer_number} reservation."
            ),
            reference_type=InventoryReferenceType.STOCK_TRANSFER,
            reference_id=stock_transfer.id,
        )

        line.source_inventory_id = inventory.id

    stock_transfer.status = TransferStatus.APPROVED

    stock_transfer.approved_by = approved_by
    stock_transfer.updated_by = approved_by

    db.commit()
    db.refresh(
        stock_transfer,
    )

    logger.info(
        "Stock Transfer %s approved successfully.",
        stock_transfer.transfer_number,
    )

    return map_stock_transfer(
        stock_transfer,
    )


def reject_stock_transfer(
    db: Session,
    stock_transfer_id: int,
    rejected_by: int,
) -> StockTransferResponse:

    logger.info(
        "Rejecting Stock Transfer id=%s",
        stock_transfer_id,
    )

    stock_transfer = _get_stock_transfer(
        db,
        stock_transfer_id,
    )

    validate_reject_stock_transfer(
        stock_transfer,
    )

    stock_transfer.status = TransferStatus.REJECTED

    stock_transfer.rejected_by = rejected_by
    stock_transfer.updated_by = rejected_by

    db.commit()
    db.refresh(
        stock_transfer,
    )

    logger.info(
        "Stock Transfer %s rejected successfully.",
        stock_transfer.transfer_number,
    )

    return map_stock_transfer(
        stock_transfer,
    )


def mark_stock_transfer_in_transit(
    db: Session,
    stock_transfer_id: int,
    updated_by: int,
) -> StockTransferResponse:

    logger.info(
        "Moving Stock Transfer id=%s to in-transit.",
        stock_transfer_id,
    )

    stock_transfer = _get_stock_transfer(
        db,
        stock_transfer_id,
    )

    validate_transit_stock_transfer(
        stock_transfer,
    )

    stock_transfer.status = TransferStatus.IN_TRANSIT

    stock_transfer.updated_by = updated_by

    db.commit()
    db.refresh(
        stock_transfer,
    )

    logger.info(
        "Stock Transfer %s is now in transit.",
        stock_transfer.transfer_number,
    )

    return map_stock_transfer(
        stock_transfer,
    )


def complete_stock_transfer(
    db: Session,
    stock_transfer_id: int,
    completed_by: int,
) -> StockTransferResponse:

    logger.info(
        "Completing Stock Transfer id=%s",
        stock_transfer_id,
    )

    stock_transfer = _get_stock_transfer(
        db,
        stock_transfer_id,
    )

    validate_complete_stock_transfer(
        stock_transfer,
    )

    for line in stock_transfer.lines:

        # --------------------------------------------
        # Source Inventory
        # --------------------------------------------

        if line.source_inventory_id is None:
            raise InvalidStockTransferException(
                f"Source inventory allocation is missing for "
                f"Stock Transfer Line '{line.id}'."
            )

        source_inventory = get_or_raise(
            find_inventory_by_id(
                db,
                line.source_inventory_id,
            ),
            InvalidStockTransferException(
                f"Source inventory with id "
                f"'{line.source_inventory_id}' was not found."
            ),
        )

        # --------------------------------------------
        # Decrease Source Inventory
        # --------------------------------------------

        decrease_inventory_transaction(
            db=db,
            inventory=source_inventory,
            quantity=line.quantity,
            current_user_id=completed_by,
            release_reserved=True,
            reason=(f"Stock Transfer " f"{stock_transfer.transfer_number} completed."),
            reference_type=InventoryReferenceType.STOCK_TRANSFER,
            reference_id=stock_transfer.id,
        )

        # --------------------------------------------
        # Destination Inventory
        # --------------------------------------------

        destination_inventory = _get_or_create_destination_inventory(
            db=db,
            line=line,
            source_inventory=source_inventory,
            destination_warehouse_id=(stock_transfer.destination_warehouse_id),
            current_user_id=completed_by,
            stock_transfer=stock_transfer,
        )

        # --------------------------------------------
        # Increase Destination Inventory
        # --------------------------------------------

        increase_inventory_transaction(
            db=db,
            inventory=destination_inventory,
            quantity=line.quantity,
            current_user_id=completed_by,
            reason=(f"Stock Transfer " f"{stock_transfer.transfer_number} completed."),
            reference_type=InventoryReferenceType.STOCK_TRANSFER,
            reference_id=stock_transfer.id,
        )

        # --------------------------------------------
        # Store Destination Inventory Allocation
        # --------------------------------------------

        line.destination_inventory_id = destination_inventory.id

    # -------------------------------------------------
    # Update Stock Transfer
    # -------------------------------------------------

    stock_transfer.status = TransferStatus.COMPLETED

    stock_transfer.completed_by = completed_by
    stock_transfer.updated_by = completed_by
    stock_transfer.completed_at = datetime.now(timezone.utc)

    # ------------------------------------------------
    # Commit Entire Transfer Atomically
    # ------------------------------------------------

    db.commit()

    db.refresh(
        stock_transfer,
    )

    logger.info(
        "Stock Transfer %s completed successfully.",
        stock_transfer.transfer_number,
    )

    return map_stock_transfer(
        stock_transfer,
    )


def cancel_stock_transfer(
    db: Session,
    stock_transfer_id: int,
    cancelled_by: int,
) -> StockTransferResponse:

    logger.info(
        "Cancelling Stock Transfer id=%s",
        stock_transfer_id,
    )

    stock_transfer = _get_stock_transfer(
        db,
        stock_transfer_id,
    )

    validate_cancel_stock_transfer(
        stock_transfer,
    )

    if stock_transfer.status == TransferStatus.APPROVED:

        for line in stock_transfer.lines:

            if line.source_inventory_id is None:
                raise InvalidStockTransferException(
                    f"Source inventory allocation is missing for "
                    f"Stock Transfer Line '{line.id}'."
                )

            source_inventory = get_or_raise(
                find_inventory_by_id(
                    db,
                    line.source_inventory_id,
                ),
                InvalidStockTransferException(
                    f"Source inventory with id "
                    f"'{line.source_inventory_id}' was not found."
                ),
            )

            release_inventory_transaction(
                db=db,
                inventory=source_inventory,
                quantity=line.quantity,
                current_user_id=cancelled_by,
                reason=(
                    f"Stock Transfer " f"{stock_transfer.transfer_number} cancelled."
                ),
                reference_type=InventoryReferenceType.STOCK_TRANSFER,
                reference_id=stock_transfer.id,
            )

    stock_transfer.status = TransferStatus.CANCELLED

    stock_transfer.cancelled_by = cancelled_by
    stock_transfer.updated_by = cancelled_by

    db.commit()
    db.refresh(
        stock_transfer,
    )

    logger.info(
        "Stock Transfer %s cancelled successfully.",
        stock_transfer.transfer_number,
    )

    return map_stock_transfer(
        stock_transfer,
    )
