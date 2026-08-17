from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise

from app.inventories.model import Inventory
from app.inventories.repository import find_duplicate_inventory

from app.products.model import Product
from app.products.repository import find_by_id as find_product_by_id

from app.warehouses.model import Warehouse
from app.warehouses.repository import find_by_id as find_warehouse_by_id

from .enums import TransferStatus
from .exceptions import (
    InsufficientStockException,
    InvalidStockTransferException,
    SourceInventoryNotFoundException,
    StockTransferCannotBeCancelledException,
    StockTransferNotApprovedException,
    StockTransferNotFoundException,
    StockTransferNotInitiatedException,
    StockTransferNotInTransitException,
    StockTransferLineNotFoundException,
)

from .model import StockTransfer, StockTransferLine
from .repository import find_stock_transfer_by_id

# ---------------------------------------------------------------------
# Entity Validation
# ---------------------------------------------------------------------


def validate_stock_transfer_exists(
    db: Session,
    stock_transfer_id: int,
) -> StockTransfer:

    return get_or_raise(
        find_stock_transfer_by_id(
            db,
            stock_transfer_id,
        ),
        StockTransferNotFoundException(
            f"Stock Transfer '{stock_transfer_id}' not found."
        ),
    )


def validate_product_exists(
    db: Session,
    product_id: int,
) -> Product:

    return get_or_raise(
        find_product_by_id(
            db,
            product_id,
        ),
        InvalidStockTransferException(f"Product '{product_id}' not found."),
    )


def validate_warehouse_exists(
    db: Session,
    warehouse_id: int,
) -> Warehouse:

    return get_or_raise(
        find_warehouse_by_id(
            db,
            warehouse_id,
        ),
        InvalidStockTransferException(f"Warehouse '{warehouse_id}' not found."),
    )


# ---------------------------------------------------------------------
# Header Validation
# ---------------------------------------------------------------------


def validate_different_warehouses(
    source_warehouse_id: int,
    destination_warehouse_id: int,
):

    if source_warehouse_id == destination_warehouse_id:
        raise InvalidStockTransferException(
            "Source warehouse and destination warehouse cannot be the same."
        )


# ---------------------------------------------------------------------
# Line Validation
# ---------------------------------------------------------------------


def validate_stock_transfer_line_exists(
    stock_transfer: StockTransfer,
    stock_transfer_line_id: int,
) -> StockTransferLine:

    stock_transfer_line = next(
        (line for line in stock_transfer.lines if line.id == stock_transfer_line_id),
        None,
    )

    return get_or_raise(
        stock_transfer_line,
        StockTransferLineNotFoundException(
            f"Stock Transfer line " f"'{stock_transfer_line_id}' not found."
        ),
    )


def validate_stock_transfer_lines(
    lines,
):

    if not lines:
        raise InvalidStockTransferException(
            "Stock Transfer must contain at least one line."
        )


def validate_transfer_quantity(
    quantity: int,
):

    if quantity <= 0:
        raise InvalidStockTransferException(
            "Transfer quantity must be greater than zero."
        )


def validate_batch_number(
    batch_number: str,
):

    if not batch_number or not batch_number.strip():
        raise InvalidStockTransferException("Batch number is required.")


def validate_duplicate_transfer_lines(
    lines,
):

    combinations = [
        (
            line.product_id,
            line.batch_number.strip(),
        )
        for line in lines
    ]

    if len(combinations) != len(set(combinations)):
        raise InvalidStockTransferException(
            "Duplicate product and batch combinations are not allowed."
        )


# ---------------------------------------------------------------------
# Inventory Validation
# ---------------------------------------------------------------------


def validate_source_inventory_exists(
    db: Session,
    product_id: int,
    warehouse_id: int,
    batch_number: str,
) -> Inventory:

    return get_or_raise(
        find_duplicate_inventory(
            db,
            product_id,
            warehouse_id,
            batch_number,
        ),
        SourceInventoryNotFoundException(
            f"Source inventory not found for product '{product_id}', "
            f"warehouse '{warehouse_id}', "
            f"batch '{batch_number}'."
        ),
    )


def validate_sufficient_stock(
    inventory: Inventory,
    quantity: int,
):

    if inventory.available_quantity < quantity:
        raise InsufficientStockException(
            f"Insufficient available stock for product "
            f"'{inventory.product_id}' and batch "
            f"'{inventory.batch_number}' for inventory '{inventory.id}'. "
            f"Available quantity: {inventory.available_quantity}, "
            f"requested quantity: {quantity}."
        )


def validate_source_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    batch_number: str,
    quantity: int,
) -> Inventory:

    inventory = validate_source_inventory_exists(
        db,
        product_id,
        warehouse_id,
        batch_number,
    )

    validate_sufficient_stock(
        inventory,
        quantity,
    )

    return inventory


# ---------------------------------------------------------------------
# Update Validation
# ---------------------------------------------------------------------


def validate_initiated_stock_transfer(
    stock_transfer: StockTransfer,
):

    if stock_transfer.status != TransferStatus.INITIATED:
        raise StockTransferNotInitiatedException(
            "Only initiated Stock Transfers can be modified."
        )


# ---------------------------------------------------------------------
# Workflow Validation
# ---------------------------------------------------------------------


def validate_approve_stock_transfer(
    stock_transfer: StockTransfer,
):

    if stock_transfer.status != TransferStatus.INITIATED:
        raise StockTransferNotInitiatedException(
            "Only initiated Stock Transfers can be approved."
        )


def validate_reject_stock_transfer(
    stock_transfer: StockTransfer,
):

    if stock_transfer.status != TransferStatus.INITIATED:
        raise StockTransferNotInitiatedException(
            "Only initiated Stock Transfers can be rejected."
        )


def validate_transit_stock_transfer(
    stock_transfer: StockTransfer,
):

    if stock_transfer.status != TransferStatus.APPROVED:
        raise StockTransferNotApprovedException(
            "Only approved Stock Transfers can be moved to transit."
        )


def validate_complete_stock_transfer(
    stock_transfer: StockTransfer,
):

    if stock_transfer.status != TransferStatus.IN_TRANSIT:
        raise StockTransferNotInTransitException(
            "Only in-transit Stock Transfers can be completed."
        )


def validate_cancel_stock_transfer(
    stock_transfer: StockTransfer,
):

    allowed_statuses = {
        TransferStatus.INITIATED,
        TransferStatus.APPROVED,
    }

    if stock_transfer.status not in allowed_statuses:
        raise StockTransferCannotBeCancelledException(
            "Only initiated or approved Stock Transfers can be cancelled."
        )
