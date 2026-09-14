from .model import Supplier
from .schema import SupplierResponse

PROFILE_COMPLETION_FIELDS = (
    "gst_number",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "supplier_type",
    "lead_time_days",
    "payment_terms",
)


def calculate_profile_completion(
    supplier: Supplier,
) -> tuple[int, bool]:

    completed_fields = sum(
        1
        for field in PROFILE_COMPLETION_FIELDS
        if getattr(supplier, field) is not None
        and str(getattr(supplier, field)).strip() != ""
    )

    total_fields = len(PROFILE_COMPLETION_FIELDS)

    percentage = round((completed_fields / total_fields) * 100)

    return percentage, percentage == 100


def map_supplier(supplier: Supplier) -> SupplierResponse:

    profile_completion_percentage, is_profile_complete = calculate_profile_completion(
        supplier
    )

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
        profile_completion_percentage=profile_completion_percentage,
        is_profile_complete=is_profile_complete,
    )


def map_suppliers(
    suppliers: list[Supplier],
) -> list[SupplierResponse]:

    return [map_supplier(supplier) for supplier in suppliers]
