from .model import UnitOfMeasure
from .schema import UnitOfMeasureResponse


def map_unit_of_measure(
    uom: UnitOfMeasure,
) -> UnitOfMeasureResponse:
    return UnitOfMeasureResponse(
        id=uom.id,
        name=uom.name,
        code=uom.code,
        is_active=uom.is_active,
        created_by=uom.created_by,
        updated_by=uom.updated_by,
        deactivated_by=uom.deactivated_by,
        reactivated_by=uom.reactivated_by,
        created_at=uom.created_at,
        updated_at=uom.updated_at,
    )


def map_units_of_measure(
    units: list[UnitOfMeasure],
) -> list[UnitOfMeasureResponse]:
    return [map_unit_of_measure(uom) for uom in units]
