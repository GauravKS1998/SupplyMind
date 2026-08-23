from app.users.enums import UserRole

READ_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.PROCUREMENT_MANAGER,
    UserRole.INVENTORY_ANALYST,
)

MANAGEMENT_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
)

APPROVAL_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.PROCUREMENT_MANAGER,
)
