from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_products: int
    total_suppliers: int
    total_warehouses: int
    total_purchase_orders: int
    total_sales_orders: int
