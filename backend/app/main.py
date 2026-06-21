from fastapi import FastAPI

from app.database.database import Base, engine

from app.products.model import Product
from app.warehouses.model import Warehouse
from app.inventories.model import Inventory

from app.products.router import router as product_router
from app.warehouses.router import router as warehouse_router
from app.inventories.router import router as inventory_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router, prefix="/products", tags=["Products"])

app.include_router(warehouse_router, prefix="/warehouses", tags=["Warehouses"])

app.include_router(inventory_router, prefix="/inventories", tags=["Inventories"])
