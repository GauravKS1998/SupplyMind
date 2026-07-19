from .model import InventoryTransaction
from .schema import InventoryTransactionResponse


def map_transaction(
    transaction: InventoryTransaction,
) -> InventoryTransactionResponse:

    return InventoryTransactionResponse(
        id=transaction.id,
        inventory_id=transaction.inventory_id,
        transaction_type=transaction.transaction_type,
        quantity_before=transaction.quantity_before,
        quantity_delta=transaction.quantity_delta,
        quantity_after=transaction.quantity_after,
        reserved_quantity_before=transaction.reserved_quantity_before,
        reserved_quantity_after=transaction.reserved_quantity_after,
        available_quantity_before=transaction.available_quantity_before,
        available_quantity_after=transaction.available_quantity_after,
        reason=transaction.reason,
        reference_type=transaction.reference_type,
        reference_id=transaction.reference_id,
        created_by=transaction.created_by,
        created_at=transaction.created_at,
    )


def map_transactions(
    transactions: list[InventoryTransaction],
):
    return [map_transaction(transaction) for transaction in transactions]
