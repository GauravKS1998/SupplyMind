from pydantic import BaseModel

class ProductCreateRequest(BaseModel):
    name: str
    price: float

class ProductUpdateRequest(BaseModel):
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float