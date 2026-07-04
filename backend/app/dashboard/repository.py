from sqlalchemy.orm import Session

from app.products.model import Product
from app.suppliers.model import Supplier
from app.warehouses.model import Warehouse
from app.purchase_orders.model import PurchaseOrder
from app.sales_orders.model import SalesOrder


def get_total_products(db: Session):
    return db.query(Product).count()


def get_total_suppliers(db: Session):
    return db.query(Supplier).count()


def get_total_warehouses(db: Session):
    return db.query(Warehouse).count()


def get_total_purchase_orders(db: Session):
    return db.query(PurchaseOrder).count()


def get_total_sales_orders(db: Session):
    return db.query(SalesOrder).count()
