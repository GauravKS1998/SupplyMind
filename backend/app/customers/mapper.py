from .model import Customer

from .schema import CustomerResponse


def map_customer(
    customer: Customer,
) -> CustomerResponse:

    return CustomerResponse(
        id=customer.id,
        user_id=customer.user_id,
        company_name=customer.company_name,
        gst_number=customer.gst_number,
        contact_person=customer.contact_person,
        phone=customer.phone,
        email=customer.email,
        address=customer.address,
        city=customer.city,
        state=customer.state,
        country=customer.country,
        postal_code=customer.postal_code,
        is_verified=customer.is_verified,
        is_active=customer.is_active,
        verified_by=customer.verified_by,
        updated_by=customer.updated_by,
        deactivated_by=customer.deactivated_by,
        deactivated_at=customer.deactivated_at,
        reactivated_by=customer.reactivated_by,
        reactivated_at=customer.reactivated_at,
        created_at=customer.created_at,
        updated_at=customer.updated_at,
    )


def map_customers(
    customers: list[Customer],
) -> list[CustomerResponse]:

    return [map_customer(customer) for customer in customers]
