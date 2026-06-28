from sqlalchemy.orm import Session

from .model import StockTransfer

from .schema import StockTransferRequest, StockTransferResponse

from .repository import find_by_product_and_warehouse, save_transfer


def transfer_stock(db: Session, request: StockTransferRequest):
    if request.source_warehouse_id == request.destination_warehouse_id:
        return {"message": "Source and destination cannot be same"}

    source_inventory = find_by_product_and_warehouse(
        db, request.product_id, request.source_warehouse_id
    )

    if not source_inventory:
        return {"message": "Source inventory not found"}

    destination_inventory = find_by_product_and_warehouse(
        db, request.product_id, request.destination_warehouse_id
    )

    if not destination_inventory:
        return {"message": "Destination inventory not found"}

    if source_inventory.quantity < request.quantity:
        return {"message": "Insufficient stock"}

    try:
        source_inventory.quantity -= request.quantity
        destination_inventory.quantity += request.quantity

        transfer = StockTransfer(
            product_id=request.product_id,
            source_warehouse_id=request.source_warehouse_id,
            destination_warehouse_id=request.destination_warehouse_id,
            quantity=request.quantity,
        )

        saved_transfer = save_transfer(db, transfer)

        db.commit()
        db.refresh(saved_transfer)

        return StockTransferResponse(
            id=saved_transfer.id,
            product_id=saved_transfer.product_id,
            source_warehouse_id=saved_transfer.source_warehouse_id,
            destination_warehouse_id=saved_transfer.destination_warehouse_id,
            quantity=saved_transfer.quantity,
            transferred_at=saved_transfer.transferred_at,
        )

    except Exception:
        db.rollback()  # Equivalent to @Transactional: if succeeds save otherwise rollback

        return {"message": "Transfer failed and rolled back"}
