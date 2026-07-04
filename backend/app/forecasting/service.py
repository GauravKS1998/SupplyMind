from sqlalchemy.orm import Session

from app.purchase_orders.model import PurchaseOrder


def forecast_product_demand(db: Session, product_id: int):
    purchase_orders = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.product_id == product_id, PurchaseOrder.status == "COMPLETED"
        )
        .all()
    )

    if not purchase_orders:
        return {"message": "No historical data found"}

    total_quantity = sum(po.quantity for po in purchase_orders)

    predicted_demand = round(total_quantity / len(purchase_orders))

    return {
        "product_id": product_id,
        "historical_orders": len(purchase_orders),
        "predicted_demand": predicted_demand,
    }
