from .model import Supplier
from .schema import SupplierResponse


def map_supplier(
    supplier: Supplier,
) -> SupplierResponse:
    return SupplierResponse(
        id=supplier.id,
        user_id=supplier.user_id,
        company_name=supplier.company_name,
        gst_number=supplier.gst_number,
        contact_person=supplier.contact_person,
        phone=supplier.phone,
        email=supplier.email,
        address=supplier.address,
        city=supplier.city,
        state=supplier.state,
        country=supplier.country,
        postal_code=supplier.postal_code,
        supplier_type=supplier.supplier_type,
        lead_time_days=supplier.lead_time_days,
        payment_terms=supplier.payment_terms,
        rating=supplier.rating,
        is_verified=supplier.is_verified,
        is_active=supplier.is_active,
    )


def map_suppliers(
    suppliers: list[Supplier],
) -> list[SupplierResponse]:
    return [map_supplier(supplier) for supplier in suppliers]
