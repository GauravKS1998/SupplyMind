from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

from app.auth.model import User
from app.categories.model import Category
from app.subcategories.model import SubCategory
from app.product_types.model import ProductType
from app.brands.model import Brand
from app.units_of_measure.model import UnitOfMeasure
from app.products.model import Product
from app.suppliers.model import Supplier
from app.warehouses.model import Warehouse
from app.inventories.model import Inventory
from app.stock_transfers.model import StockTransfer
from app.purchase_orders.model import PurchaseOrder
from app.sales_orders.model import SalesOrder

from app.dashboard.router import router as dashboard_router
from app.categories.router import router as category_router
from app.subcategories.router import router as subcategory_router
from app.product_types.router import router as product_type_router
from app.products.router import router as product_router
from app.suppliers.router import router as supplier_router
from app.warehouses.router import router as warehouse_router
from app.inventories.router import router as inventory_router
from app.stock_transfers.router import router as stock_transfer_router
from app.purchase_orders.router import router as purchase_order_router
from app.sales_orders.router import router as sales_order_router
from app.forecasting.router import router as forecasting_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

app.include_router(category_router, prefix="/categories", tags=["Categories"])

app.include_router(subcategory_router, prefix="/subcategories", tags=["SubCategories"])

app.include_router(product_type_router, prefix="/product-types", tags=["Product Types"])

app.include_router(product_router, prefix="/products", tags=["Products"])

app.include_router(supplier_router, prefix="/suppliers", tags=["Suppliers"])

app.include_router(warehouse_router, prefix="/warehouses", tags=["Warehouses"])

app.include_router(inventory_router, prefix="/inventories", tags=["Inventories"])

app.include_router(
    stock_transfer_router, prefix="/stock-transfers", tags=["Stock Transfers"]
)

app.include_router(
    purchase_order_router, prefix="/purchase-orders", tags=["Purchase Orders"]
)

app.include_router(sales_order_router, prefix="/sales-orders", tags=["Sales Orders"])

app.include_router(forecasting_router, prefix="/forecasting", tags=["Forecasting"])
