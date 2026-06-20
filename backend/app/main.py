from fastapi import FastAPI

from app.database.database import (
    Base,
    engine
)

from app.products.model import Product
from app.warehouses.model import Warehouse

from app.products.router import router as product_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    product_router,
    prefix="/products",
    tags=["Products"]
)