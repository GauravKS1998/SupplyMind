from sqlalchemy.orm import Session

from app.purchase_orders.model import PurchaseOrder

from app.categories.repository import find_by_id as find_category_by_id
from app.subcategories.repository import find_by_id as find_subcategory_by_id
from app.product_types.repository import find_by_id as find_product_type_by_id
from app.products.repository import find_by_id as find_product_by_id
from app.suppliers.repository import find_by_id as find_supplier_by_id


def forecast_product_demand(db: Session, product_id: int):
    product = find_product_by_id(db, product_id)

    if not product:
        return {"message": "Product not found"}

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
        "product_name": purchase_orders[0].product.name,
        "product_sku": purchase_orders[0].product.sku,
        "supplier_name": purchase_orders[0].product.supplier.name,
        "category_name": purchase_orders[0].product.category.name,
        "subcategory_name": purchase_orders[0].product.subcategory.name,
        "product_type_name": purchase_orders[0].product.product_type.name,
        "historical_orders": len(purchase_orders),
        "predicted_demand": predicted_demand,
    }


def forecast_by_supplier(db: Session, supplier_id: int):
    supplier = find_supplier_by_id(db, supplier_id)

    if not supplier:
        return {"message": "Supplier not found"}

    purchase_orders = (
        db.query(PurchaseOrder)
        .join(PurchaseOrder.product)
        .filter(
            PurchaseOrder.status == "COMPLETED",
            PurchaseOrder.product.has(supplier_id=supplier_id),
        )
        .all()
    )

    if not purchase_orders:
        return {"message": "No historical supplier data found"}

    total_quantity = sum(po.quantity for po in purchase_orders)

    predicted_demand = round(total_quantity / len(purchase_orders))

    return {
        "supplier_name": purchase_orders[0].product.supplier.name,
        "historical_orders": len(purchase_orders),
        "predicted_demand": predicted_demand,
    }


def forecast_by_category(db: Session, category_id: int):
    category = find_category_by_id(db, category_id)

    if not category:
        return {"message": "Category not found"}

    purchase_orders = (
        db.query(PurchaseOrder)
        .join(PurchaseOrder.product)
        .filter(
            PurchaseOrder.status == "COMPLETED",
            PurchaseOrder.product.has(category_id=category_id),
        )
        .all()
    )

    if not purchase_orders:
        return {"message": "No historical category data found"}

    total_quantity = sum(po.quantity for po in purchase_orders)

    predicted_demand = round(total_quantity / len(purchase_orders))

    return {
        "category_name": purchase_orders[0].product.category.name,
        "historical_orders": len(purchase_orders),
        "predicted_demand": predicted_demand,
    }


def forecast_by_subcategory(db: Session, subcategory_id: int):
    subcategory = find_subcategory_by_id(db, subcategory_id)

    if not subcategory:
        return {"message": "Sub-category not found"}

    purchase_orders = (
        db.query(PurchaseOrder)
        .join(PurchaseOrder.product)
        .filter(
            PurchaseOrder.status == "COMPLETED",
            PurchaseOrder.product.has(subcategory_id=subcategory_id),
        )
        .all()
    )

    if not purchase_orders:
        return {"message": "No historical sub-category data found"}

    total_quantity = sum(po.quantity for po in purchase_orders)

    predicted_demand = round(total_quantity / len(purchase_orders))

    return {
        "sub_category_name": purchase_orders[0].product.subcategory.name,
        "historical_orders": len(purchase_orders),
        "predicted_demand": predicted_demand,
    }


def forecast_by_product_type(db: Session, product_type_id: int):
    product_type = find_product_type_by_id(db, product_type_id)

    if not product_type:
        return {"message": "Category not found"}

    purchase_orders = (
        db.query(PurchaseOrder)
        .join(PurchaseOrder.product)
        .filter(
            PurchaseOrder.status == "COMPLETED",
            PurchaseOrder.product.has(product_type_id=product_type_id),
        )
        .all()
    )

    if not purchase_orders:
        return {"message": "No historical product type data found"}

    total_quantity = sum(po.quantity for po in purchase_orders)

    predicted_demand = round(total_quantity / len(purchase_orders))

    return {
        "product_type": purchase_orders[0].product.product_type.name,
        "historical_orders": len(purchase_orders),
        "predicted_demand": predicted_demand,
    }
