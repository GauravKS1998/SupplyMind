from sqlalchemy.orm import Session

from .repository import find_by_id
from .exceptions import InventoryTransactionNotFoundException


def validate_transaction_exists(
    db: Session,
    transaction_id: int,
):
    transaction = find_by_id(
        db,
        transaction_id,
    )

    if not transaction:
        raise InventoryTransactionNotFoundException(
            f"Inventory transaction {transaction_id} not found."
        )

    return transaction
