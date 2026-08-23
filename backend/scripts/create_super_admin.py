from getpass import getpass

from app.auth.jwt import hash_password
from app.database.database import SessionLocal
from app.users.enums import ApprovalStatus, UserRole
from app.users.model import User
from app.users.repository import find_by_email


def create_super_admin():
    db = SessionLocal()

    try:
        print("\n=== SupplyMind Super Admin Bootstrap ===\n")

        existing_super_admin = (
            db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
        )

        if existing_super_admin:
            print(f"SUPER_ADMIN already exists: " f"{existing_super_admin.email}")
            print("Bootstrap cancelled.")
            return

        full_name = input("Full name: ").strip()
        email = input("Email: ").strip().lower()
        phone = input("Phone (optional): ").strip() or None

        if find_by_email(db, email):
            print(f"\nA user with email '{email}' already exists.")
            print("Bootstrap cancelled.")
            return

        password = getpass("Password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("\nPasswords do not match.")
            return

        if len(password) < 8:
            print("\nPassword must contain at least 8 characters.")
            return

        print(f"\nPassword: {password}")

        super_admin = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            role=UserRole.SUPER_ADMIN,
            approval_status=ApprovalStatus.APPROVED,
            is_active=True,
        )

        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)

        print("\nSUPER_ADMIN created successfully.")
        print(f"ID: {super_admin.id}")
        print(f"Name: {super_admin.full_name}")
        print(f"Email: {super_admin.email}")
        print(f"Role: {super_admin.role}")
        print(f"Status: {super_admin.approval_status}")
        print(f"Active: {super_admin.is_active}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_super_admin()
