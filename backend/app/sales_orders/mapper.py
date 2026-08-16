from app.sales_orders.model import (
    SalesOrder,
    SalesOrderLine,
)

from app.sales_orders.schema import SalesOrderLineResponse, SalesOrderResponse

from app.purchase_orders.schema import (
    ProductSummary,
    UomSummary,
    WarehouseSummary,
)


def map_sales_order_line(
    line: SalesOrderLine,
) -> SalesOrderLineResponse:

    return SalesOrderLineResponse(
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
        unit_price=line.unit_price,
        discount_amount=line.discount_amount,
        tax_amount=line.tax_amount,
        line_total=line.line_total,
        remarks=line.remarks,
    )


def map_sales_order(
    sales_order: SalesOrder,
) -> SalesOrderResponse:

    return SalesOrderResponse(
        id=sales_order.id,
        so_number=sales_order.so_number,
        customer_id=sales_order.customer_id,
        warehouse=WarehouseSummary(
            id=sales_order.warehouse.id,
            warehouse_code=sales_order.warehouse.warehouse_code,
            warehouse_name=sales_order.warehouse.warehouse_name,
        ),
        status=sales_order.status,
        subtotal=sales_order.subtotal,
        discount_total=sales_order.discount_total,
        tax_total=sales_order.tax_total,
        grand_total=sales_order.grand_total,
        remarks=sales_order.remarks,
        created_by=sales_order.created_by,
        confirmed_by=sales_order.confirmed_by,
        dispatched_by=sales_order.dispatched_by,
        delivered_by=sales_order.delivered_by,
        completed_by=sales_order.completed_by,
        cancelled_by=sales_order.cancelled_by,
        returned_by=sales_order.returned_by,
        updated_by=sales_order.updated_by,
        created_at=sales_order.created_at,
        updated_at=sales_order.updated_at,
        delivered_at=sales_order.delivered_at,
        completed_at=sales_order.completed_at,
        returned_at=sales_order.returned_at,
        lines=[map_sales_order_line(line) for line in sales_order.lines],
    )


def map_sales_orders(
    sales_orders: list[SalesOrder],
) -> list[SalesOrderResponse]:

    return [map_sales_order(sales_order) for sales_order in sales_orders]
