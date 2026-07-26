from app.purchase_orders.model import PurchaseOrder
from app.purchase_orders.schema import (
    ProductSummary,
    PurchaseOrderLineResponse,
    PurchaseOrderResponse,
    SupplierSummary,
    UomSummary,
    WarehouseSummary,
)


def map_purchase_order_line(
    line,
) -> PurchaseOrderLineResponse:

    return PurchaseOrderLineResponse(
        id=line.id,
        line_number=line.line_number,
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
        product_name_snapshot=line.product_name_snapshot,
        product_sku_snapshot=line.product_sku_snapshot,
        ordered_quantity=line.ordered_quantity,
        received_quantity=line.received_quantity,
        unit_price=line.unit_price,
        discount_amount=line.discount_amount,
        tax_amount=line.tax_amount,
        line_total=line.line_total,
        remarks=line.remarks,
    )


def map_purchase_order(
    purchase_order: PurchaseOrder,
) -> PurchaseOrderResponse:

    return PurchaseOrderResponse(
        id=purchase_order.id,
        po_number=purchase_order.po_number,
        supplier=SupplierSummary(
            id=purchase_order.supplier.id,
            supplier_code=purchase_order.supplier.supplier_code,
            supplier_name=purchase_order.supplier.supplier_name,
        ),
        warehouse=WarehouseSummary(
            id=purchase_order.warehouse.id,
            warehouse_code=purchase_order.warehouse.warehouse_code,
            warehouse_name=purchase_order.warehouse.warehouse_name,
        ),
        status=purchase_order.status,
        expected_delivery_date=purchase_order.expected_delivery_date,
        subtotal=purchase_order.subtotal,
        discount_total=purchase_order.discount_total,
        tax_total=purchase_order.tax_total,
        grand_total=purchase_order.grand_total,
        remarks=purchase_order.remarks,
        created_at=purchase_order.created_at,
        updated_at=purchase_order.updated_at,
        lines=[map_purchase_order_line(line) for line in purchase_order.lines],
    )


def map_purchase_orders(
    purchase_orders: list[PurchaseOrder],
) -> list[PurchaseOrderResponse]:

    return [map_purchase_order(po) for po in purchase_orders]
