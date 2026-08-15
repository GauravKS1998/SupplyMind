from app.goods_receipts.model import GoodsReceipt
from app.goods_receipts.schema import (
    GoodsReceiptLineResponse,
    GoodsReceiptResponse,
    PurchaseOrderSummary,
    WarehouseSummary,
)
from app.purchase_orders.schema import ProductSummary, UomSummary


def map_goods_receipt_line(
    line,
) -> GoodsReceiptLineResponse:

    return GoodsReceiptLineResponse(
        id=line.id,
        line_number=line.line_number,
        purchase_order_line_id=line.purchase_order_line_id,
        product=ProductSummary(
            id=line.product.id,
            sku=line.product.sku,
            name=line.product.name,
            uom=UomSummary(
                id=line.product.uom.id,
                code=line.product.uom.code,
                name=line.product.uom.name,
            ),
        ),
        batch_number=line.batch_number,
        accepted_quantity=line.accepted_quantity,
        rejected_quantity=line.rejected_quantity,
        remarks=line.remarks,
    )


def map_goods_receipt(
    goods_receipt: GoodsReceipt,
) -> GoodsReceiptResponse:

    return GoodsReceiptResponse(
        id=goods_receipt.id,
        grn_number=goods_receipt.grn_number,
        purchase_order=PurchaseOrderSummary(
            id=goods_receipt.purchase_order.id,
            po_number=goods_receipt.purchase_order.po_number,
        ),
        warehouse=WarehouseSummary(
            id=goods_receipt.warehouse.id,
            warehouse_code=goods_receipt.warehouse.warehouse_code,
            warehouse_name=goods_receipt.warehouse.warehouse_name,
        ),
        status=goods_receipt.status,
        remarks=goods_receipt.remarks,
        created_by=goods_receipt.created_by,
        received_by=goods_receipt.received_by,
        approved_by=goods_receipt.approved_by,
        cancelled_by=goods_receipt.cancelled_by,
        updated_by=goods_receipt.updated_by,
        created_at=goods_receipt.created_at,
        updated_at=goods_receipt.updated_at,
        lines=[map_goods_receipt_line(line) for line in goods_receipt.lines],
    )


def map_goods_receipts(
    goods_receipts: list[GoodsReceipt],
) -> list[GoodsReceiptResponse]:

    return [map_goods_receipt(goods_receipt) for goods_receipt in goods_receipts]
