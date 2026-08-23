from app.users.enums import UserRole

READ_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.SALES_MANAGER,
    UserRole.INVENTORY_ANALYST,
)

MANAGEMENT_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
)

APPROVAL_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.SALES_MANAGER,
)
