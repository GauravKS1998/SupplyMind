from app.stock_transfers.model import (
    StockTransfer,
    StockTransferLine,
)

from app.stock_transfers.schema import (
    StockTransferLineResponse,
    StockTransferResponse,
)

from app.purchase_orders.schema import (
    ProductSummary,
    UomSummary,
    WarehouseSummary,
)


def map_stock_transfer_line(
    line: StockTransferLine,
) -> StockTransferLineResponse:

    return StockTransferLineResponse(
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
        batch_number=line.batch_number,
        quantity=line.quantity,
        remarks=line.remarks,
    )


def map_stock_transfer(
    stock_transfer: StockTransfer,
) -> StockTransferResponse:

    return StockTransferResponse(
        id=stock_transfer.id,
        transfer_number=stock_transfer.transfer_number,
        source_warehouse=WarehouseSummary(
            id=stock_transfer.source_warehouse.id,
            warehouse_code=stock_transfer.source_warehouse.warehouse_code,
            warehouse_name=stock_transfer.source_warehouse.warehouse_name,
        ),
        destination_warehouse=WarehouseSummary(
            id=stock_transfer.destination_warehouse.id,
            warehouse_code=stock_transfer.destination_warehouse.warehouse_code,
            warehouse_name=stock_transfer.destination_warehouse.warehouse_name,
        ),
        status=stock_transfer.status,
        remarks=stock_transfer.remarks,
        initiated_by=stock_transfer.initiated_by,
        approved_by=stock_transfer.approved_by,
        rejected_by=stock_transfer.rejected_by,
        cancelled_by=stock_transfer.cancelled_by,
        completed_by=stock_transfer.completed_by,
        updated_by=stock_transfer.updated_by,
        created_at=stock_transfer.created_at,
        updated_at=stock_transfer.updated_at,
        completed_at=stock_transfer.completed_at,
        lines=[map_stock_transfer_line(line) for line in stock_transfer.lines],
    )


def map_stock_transfers(
    stock_transfers: list[StockTransfer],
) -> list[StockTransferResponse]:

    return [map_stock_transfer(stock_transfer) for stock_transfer in stock_transfers]
