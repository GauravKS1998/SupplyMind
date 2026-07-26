from enum import Enum


class DocumentType(Enum):
    PURCHASE_ORDER = "PO"
    SALES_ORDER = "SO"
    GOODS_RECEIPT = "GRN"
    STOCK_TRANSFER = "ST"
    STOCK_ADJUSTMENT = "SA"
    PURCHASE_RETURN = "PR"
    SALES_RETURN = "SR"
    INVENTORY_COUNT = "IC"
