from fastapi import FastAPI

from app.database.database import Base, engine

from app.products.model import Product
from app.warehouses.model import Warehouse

from app.products.router import router as product_router
from app.warehouses.router import router as warehouse_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router, prefix="/products", tags=["Products"])

app.include_router(warehouse_router, prefix="/warehouses", tags=["Warehouses"])
