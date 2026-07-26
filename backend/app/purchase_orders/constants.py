from app.users.enums import UserRole

READ_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.PROCUREMENT_MANAGER,
)

MANAGEMENT_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.PROCUREMENT_MANAGER,
)

APPROVAL_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.FINANCE_MANAGER,
)
