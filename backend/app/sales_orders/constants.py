from app.users.enums import UserRole

READ_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.SALES_MANAGER,
    UserRole.FINANCE_MANAGER,
)


MANAGEMENT_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.SALES_MANAGER,
)


APPROVAL_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.SALES_MANAGER,
)


RESERVATION_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.WAREHOUSE_MANAGER,
    UserRole.WAREHOUSE_STAFF,
)


DELIVERY_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.SALES_MANAGER,
)


CUSTOMER_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.SALES_MANAGER,
    UserRole.CUSTOMER,
)
