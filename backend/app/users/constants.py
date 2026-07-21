from .enums import UserRole

INTERNAL_ROLES = {
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.PROCUREMENT_MANAGER,
    UserRole.WAREHOUSE_MANAGER,
    UserRole.WAREHOUSE_STAFF,
    UserRole.SALES_MANAGER,
    UserRole.FINANCE_MANAGER,
    UserRole.INVENTORY_ANALYST,
}

EXTERNAL_ROLES = {UserRole.SUPPLIER, UserRole.CUSTOMER}
