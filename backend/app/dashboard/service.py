from sqlalchemy.orm import Session

from .schema import DashboardSummaryResponse

from .repository import (
    get_total_products,
    get_total_suppliers,
    get_total_warehouses,
    get_total_purchase_orders,
    get_total_sales_orders,
)


def get_dashboard_summary(db: Session) -> DashboardSummaryResponse:
    total_products = get_total_products(db)
    total_suppliers = get_total_suppliers(db)
    total_warehouses = get_total_warehouses(db)
    total_purchase_orders = get_total_purchase_orders(db)
    total_sales_orders = get_total_sales_orders(db)

    return DashboardSummaryResponse(
        total_products=total_products,
        total_suppliers=total_suppliers,
        total_warehouses=total_warehouses,
        total_purchase_orders=total_purchase_orders,
        total_sales_orders=total_sales_orders,
    )
