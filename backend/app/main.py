from fastapi import FastAPI

from app.database.database import Base, engine

from app.products.model import Product
from app.warehouses.model import Warehouse
from app.inventories.model import Inventory
from app.stock_transfers.model import StockTransfer

from app.products.router import router as product_router
from app.warehouses.router import router as warehouse_router
from app.inventories.router import router as inventory_router
from app.stock_transfers.router import router as stock_transfer_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router, prefix="/products", tags=["Products"])

app.include_router(warehouse_router, prefix="/warehouses", tags=["Warehouses"])

app.include_router(inventory_router, prefix="/inventories", tags=["Inventories"])

app.include_router(
    stock_transfer_router, prefix="/stock-transfers", tags=["Stock Transfers"]
)
