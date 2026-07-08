from sqlalchemy.orm import Session

from .model import PurchaseOrder
from .schema import PurchaseOrderCreateRequest, PurchaseOrderResponse

from .repository import find_all, find_by_id, save, find_by_po_number

from app.suppliers.repository import find_by_id as find_supplier_by_id

from app.products.repository import find_by_id as find_product_by_id

from app.warehouses.repository import find_by_id as find_warehouse_by_id

from app.inventories.repository import (
    find_by_product_and_warehouse,
    save as save_inventory,
)

from app.inventories.model import Inventory

from .enums import PurchaseOrderStatus

from .exceptions import (
    PurchaseOrderAlreadyExistsException,
    PurchaseOrderCannotBeCancelledException,
    PurchaseOrderFailException,
    PurchaseOrderNotApprovedException,
    PurchaseOrderNotDraftedException,
    PurchaseOrderNotInTransitException,
    PurchaseOrderNotOrderedException,
    PurchaseOrderNotReceivedException,
    PurchaseOrderNotSubmittedException,
    PurchaseOrderNotFoundException,
)
from app.inventories.exceptions import InventoryNotFoundException

from app.logging.logger import logger


def map_purchase_order_response(po):
    return PurchaseOrderResponse(
        id=po.id,
        po_number=po.po_number,
        supplier_id=po.supplier.id,
        supplier_name=po.supplier.company_name,
        product_id=po.product.id,
        product_name=po.product.name,
        product_sku=po.product.sku,
        warehouse_id=po.warehouse.id,
        warehouse_name=po.warehouse.name,
        quantity=po.quantity,
        status=po.status,
        expected_delivery_date=po.expected_delivery_date,
        actual_delivery_date=po.actual_delivery_date,
        created_by=po.created_by,
        approved_by=po.approved_by,
        closed_by=po.closed_by,
        cancelled_by=po.cancelled_by,
        rejected_by=po.rejected_by,
        updated_by=po.updated_by,
        updated_at=po.updated_at,
        created_at=po.created_at,
    )


def get_all_purchase_orders(db: Session):
    purchase_orders = find_all(db)

    return [map_purchase_order_response(po) for po in purchase_orders]


def create_draft_po(
    db: Session, request: PurchaseOrderCreateRequest, current_user_id: int
):
    existing_po = find_by_po_number(db, request.po_number)

    if existing_po:
        raise PurchaseOrderAlreadyExistsException("PO number already exists")

    try:
        po = PurchaseOrder(
            po_number=request.po_number,
            supplier_id=request.supplier_id,
            product_id=request.product_id,
            warehouse_id=request.warehouse_id,
            quantity=request.quantity,
            expected_delivery_date=request.expected_delivery_date,
            created_by=current_user_id,
            status=PurchaseOrderStatus.DRAFT,
        )

        saved_po = save(db, po)

        db.commit()
        db.refresh(saved_po)

        saved_po = find_by_id(db, saved_po.id)

        logger.info(f"Purchase order draft {saved_po.id} created")

        return map_purchase_order_response(saved_po)

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to create purchase order")


def submit_po(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status != PurchaseOrderStatus.DRAFT:
        raise PurchaseOrderNotDraftedException("Only draft PO can be submitted")

    try:
        po.status = PurchaseOrderStatus.SUBMITTED
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} submitted")

        return {"message": "Purchase order submitted successfully"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to submit purchase order")


def approve_po(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status != PurchaseOrderStatus.SUBMITTED:
        raise PurchaseOrderNotSubmittedException("Only submitted PO can be approved")

    try:
        po.status = PurchaseOrderStatus.APPROVED
        po.approved_by = current_user_id
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} approved")

        return {"message": "Purchase order approved successfully"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to approve purchase order")


def reject_po(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status != PurchaseOrderStatus.SUBMITTED:
        raise PurchaseOrderNotSubmittedException("Only submitted PO can be rejected")

    try:
        po.status = PurchaseOrderStatus.REJECTED
        po.rejected_by = current_user_id
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} rejected")

        return {"message": "Purchase order rejected successfully"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to reject purchase order")


def mark_ordered(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status != PurchaseOrderStatus.APPROVED:
        raise PurchaseOrderNotApprovedException(
            "Only approved PO can be marked ordered"
        )

    try:
        po.status = PurchaseOrderStatus.ORDERED
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} ordered")

        return {"message": "Purchase order marked as ordered"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to mark purchase order as ordered")


def mark_in_transit(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status != PurchaseOrderStatus.ORDERED:
        raise PurchaseOrderNotOrderedException("Only ordered PO can move to transit")

    try:
        po.status = PurchaseOrderStatus.IN_TRANSIT
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} in transit")

        return {"message": "Purchase order is now in transit"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to mark purchase order as in transit")


from datetime import datetime, timezone


def receive_po(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status != PurchaseOrderStatus.IN_TRANSIT:
        raise PurchaseOrderNotInTransitException("Only in-transit PO can be received")

    inventory = find_by_product_and_warehouse(db, po.product_id, po.warehouse_id)

    if not inventory:
        raise InventoryNotFoundException("Inventory not found")

    try:
        inventory.quantity += po.quantity
        inventory.available_quantity += po.quantity

        po.status = PurchaseOrderStatus.RECEIVED
        po.actual_delivery_date = datetime.now(timezone.utc)
        po.received_by = current_user_id
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} received")

        return {"message": "Purchase order received successfully"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to receive purchase order")


def close_po(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status != PurchaseOrderStatus.RECEIVED:
        raise PurchaseOrderNotReceivedException("Only received PO can be closed")

    try:
        po.status = PurchaseOrderStatus.CLOSED
        po.closed_by = current_user_id
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} closed")

        return {"message": "Purchase order closed successfully"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to close purchase order")


def cancel_po(db: Session, po_id: int, current_user_id: int):
    po = find_by_id(db, po_id)

    if not po:
        raise PurchaseOrderNotFoundException("Purchase order not found")

    if po.status not in {
        PurchaseOrderStatus.DRAFT,
        PurchaseOrderStatus.APPROVED,
        PurchaseOrderStatus.ORDERED,
    }:
        raise PurchaseOrderCannotBeCancelledException(
            "PO cannot be cancelled in current state"
        )

    try:
        po.status = PurchaseOrderStatus.CANCELLED
        po.cancelled_by = current_user_id
        po.updated_by = current_user_id
        po.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(po)

        logger.info(f"Purchase order {po.id} cancelled successfully")

        return {"message": "Purchase order cancelled"}

    except Exception:
        db.rollback()
        raise PurchaseOrderFailException("Failed to cancel purchase order")
